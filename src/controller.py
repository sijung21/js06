#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

import json
import os
import sys
from typing import List

import cv2
import numpy as np
# import onnxruntime as ort

from PyQt5.QtCore import (QDateTime, QDir, QObject, QRect, QThread,
                          QThreadPool, QTime, QTimer, pyqtSignal, pyqtSlot)
from PyQt5.QtGui import QImage
from PyQt5.QtMultimedia import QVideoFrame

from .model import (Js08AttrModel, , Js08IoRunner,
                    Js08Settings, Js08SimpleTarget, Js08Wedge)


class JS06MainCtrl(QObject):
    abnormal_shutdown = pyqtSignal()
    front_camera_changed = pyqtSignal(str) # uri
    rear_camera_changed = pyqtSignal(str) # uri
    front_target_decomposed = pyqtSignal()
    rear_target_decomposed = pyqtSignal()
    target_assorted = pyqtSignal(list, list) # positives, negatives
    wedge_vis_ready = pyqtSignal(int, dict) # epoch, wedge visibility

    # def __init__(self, model: Js08AttrModel):
    def __init__(self):
        super().__init__()

        self.writer_pool = QThreadPool.globalInstance()
        self.writer_pool.setMaxThreadCount(1)

        self._model = model

        self.num_working_cam = 0

        self.front_simple_targets = []
        self.rear_simple_targets = []

        self.front_target_prepared = False
        self.rear_target_prepared = False

        self.init_db()

        self.observation_timer = QTimer(self)
        # self.front_camera_changed.connect(self.decompose_front_targets)
        # self.rear_camera_changed.connect(self.decompose_rear_targets)

        self.worker_running = False
        self.start_observation_timer()

    def init_db(self):
        # db_host = Js08Settings.get('db_host')
        # db_port = Js08Settings.get('db_port')
        # db_name = Js08Settings.get('db_name')
        # self._model.connect_to_db(db_host, db_port, db_name)

        if getattr(sys, 'frozen', False):
            directory = sys._MEIPASS
        else:
            directory = os.path.dirname(__file__)
        attr_path = os.path.join(directory, 'resources', 'attr.json')
        with open(attr_path, 'r') as f:
            attr_json = json.load(f)
        camera_path = os.path.join(directory, 'resources', 'camera.json')
        with open(camera_path, 'r') as f:
            camera_json = json.load(f)

        self._model.setup_db(attr_json, camera_json)

    @pyqtSlot(str)
    def decompose_front_targets(self, _: str) -> None:
        """Make list of SimpleTarget by decoposing compound targets.

        Parameters:
        """
        self.front_target_prepared = False
        # self.decompose_targets('front')
        self.front_target_prepared = True

    @pyqtSlot(str)
    def decompose_rear_targets(self, _: str) -> None:
        """Make list of SimpleTarget by decoposing compound targets.

        Parameters:
        """
        self.rear_target_prepared = False
        # self.decompose_targets('rear')
        self.rear_target_prepared = True

    def decompose_targets(self, direction: str) -> None:
        """Make list of SimpleTarget by decoposing compound targets.

        Parameters:
            direction: 'front' or 'rear', default is 'front'
        """
        decomposed_targets = []
        attr = self._model.read_attr()
        if direction == 'front':
            targets = attr['front_camera']['targets']
            id = str(attr['front_camera']['camera_id'])
        elif direction == 'rear':
            targets = attr['rear_camera']['targets']
            id = str(attr['rear_camera']['camera_id'])
        
        base_path = Js08Settings.get('image_base_path') 
        
        # Prepare model.
        # TODO(Kyungwon): Put the model file into Qt Resource Collection.
        if getattr(sys, 'frozen', False):
            directory = sys._MEIPASS
        else:
            directory = os.path.dirname(__file__)
        model_path = os.path.join(directory, 'resources', 'js08_1636343249.onnx')
        providers = ['CPUExecutionProvider']
        sess = ort.InferenceSession(model_path, providers=providers)
        input_shape = sess.get_inputs()[0].shape
        input_height = input_shape[1]
        input_width = input_shape[2]
        
        for tg in targets:
            wedge = tg['wedge']
            azimuth = tg['azimuth']
            point = tg['roi']['point']
            size = tg['roi']['size']
            roi = QRect(*point, *size)

            for i in range(len(tg['mask'])):
                label = f"{tg['label']}-{i}"
                distance = tg['distance'][i]
                mask_path = os.path.join(base_path, 'mask', id, tg['mask'][i])
                mask = self.read_mask(mask_path)
                st = Js08SimpleTarget(label, wedge, azimuth, distance, roi, mask, input_width, input_height)
                decomposed_targets.append(st)

        if direction == 'front':
            self.front_simple_targets = decomposed_targets
        elif direction == 'rear':
            self.rear_simple_targets = decomposed_targets

    def read_mask(self, path: str) -> np.ndarray:
        """Read mask image and return 

        Parameters:
            path: path to mask file
        """
        attr = self._model.read_attr()
        front_id = str(attr['front_camera']['camera_id'])
        rear_id = str(attr['rear_camera']['camera_id'])

        basepath = Js08Settings.get('image_base_path')
        front_dir = os.path.join(basepath, 'mask', front_id)
        rear_dir = os.path.join(basepath, 'mask', rear_id)
        os.makedirs(front_dir, exist_ok=True)
        os.makedirs(rear_dir, exist_ok=True)

        with open(path, 'rb') as f:
            content = f.read()
        image = QImage()
        image.loadFromData(content)
        return image

    def start_observation_timer(self) -> None:
        print('DEBUG(start_observation_timer):', QTime.currentTime().toString())
        self.observation_timer.setInterval(1000) # every one second
        self.observation_timer.timeout.connect(self.start_worker)
        self.observation_timer.start()

    @pyqtSlot()
    def start_worker(self) -> None:
        # if decomposed targets are not ready, quit.
        if self.front_target_prepared is False or self.rear_target_prepared is False:
            return

        # If broker is already running, quit.
        if self.worker_running:
            return
        else:
            self.worker_running = True

        self.epoch = QDateTime.currentSecsSinceEpoch()
        front_uri = self.get_front_camera_uri()
        rear_uri = self.get_rear_camera_uri()
        self.worker = Js08InferenceWorker(
            self.epoch,
            front_uri, 
            rear_uri, 
            self.front_simple_targets, 
            self.rear_simple_targets
            )
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.postproduction)
        self.worker.finished.connect(self.finalize_broker)
        self.worker_thread.start()

    @pyqtSlot()
    def finalize_broker(self):
        self.worker_running = False

    @pyqtSlot()
    def postproduction(self):
        """
        epoch: seconds since epoch
        """
        epoch = self.epoch
            
        pos, neg = self.assort_discernment()
        self.target_assorted.emit(pos, neg)
        wedge_vis = self.wedge_visibility()
        self.wedge_vis_ready.emit(epoch, wedge_vis)
        self.write_visibilitiy(epoch, wedge_vis)
        self._model.write_discernment(epoch, self.front_simple_targets, self.rear_simple_targets)

    @pyqtSlot()
    def stop_timer(self) -> None:
        self.observation_timer.stop()

    def assort_discernment(self) -> tuple:
        """Assort targets in positive or negative according to the discernment result
        """
        pos, neg = [], []

        for t in self.front_simple_targets:
            point = (t.azimuth, t.distance)
            if t.discernment:
                pos.append(point)
            else:
                neg.append(point)

        for t in self.rear_simple_targets:
            point = (t.azimuth, t.distance)
            if t.discernment:
                pos.append(point)
            else:
                neg.append(point)

        return pos, neg

    def write_visibilitiy(self, epoch: int, wedge_visibility: dict) -> None:
        wedge_visibility = wedge_visibility.copy()
        vis_list = list(wedge_visibility.values())
        prevailing = self.prevailing_visibility(vis_list)
        wedge_visibility['epoch'] = epoch
        wedge_visibility['prevailing'] = prevailing
        print('DEBUG:', wedge_visibility)
        self._model.write_visibility(wedge_visibility)

    def wedge_visibility(self) -> dict:
        wedge_vis = {w: None for w in Js08Wedge}
        for t in self.front_simple_targets:
            if t.discernment:
                if wedge_vis[t.wedge] == None:
                    wedge_vis[t.wedge] = t.distance
                elif wedge_vis[t.wedge] < t.distance:
                    wedge_vis[t.wedge] = t.distance
        for t in self.rear_simple_targets:
            if t.discernment:
                if wedge_vis[t.wedge] == None:
                    wedge_vis[t.wedge] = t.distance
                elif wedge_vis[t.wedge] < t.distance:
                    wedge_vis[t.wedge] = t.distance
        return wedge_vis

    def prevailing_visibility(self, wedge_vis: list) -> float:
        if None in wedge_vis:
            return None
        sorted_vis = sorted(wedge_vis, reverse=True)
        prevailing = sorted_vis[(len(sorted_vis) - 1) // 2]
        return prevailing

    def save_image(self, dir: str, filename: str, image: QImage) -> None:
        os.makedirs(dir, exist_ok=True)
        path = QDir.cleanPath(os.path.join(dir, filename))
        runner = Js08IoRunner(path, image)
        self.writer_pool.start(runner)
    
    def grab_image(self, direction: str) -> QImage:
        """
        Parameters:
            direction: 'front' or 'rear'
        """
        if direction == 'front':
            uri = self.get_front_camera_uri()
        elif direction == 'rear':
            uri = self.get_rear_camera_uri()
        cap = cv2.VideoCapture(uri)
        ret, frame = cap.read()
        image = None
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        return image

    @pyqtSlot()
    def get_front_camera_uri(self) -> str:
        attr = self._model.read_attr()
        return attr['front_camera']['uri']

    @pyqtSlot()
    def get_rear_camera_uri(self) -> str:
        attr = self._model.read_attr()
        return attr['rear_camera']['uri']

    def get_target(self, direction: str) -> list:
        attr = self._model.read_attr()
        return attr[f'{direction}_camera']['targets']

    def get_camera_table_model(self) -> dict:
        cameras = self.get_cameras()
        table_model =  Js08CameraTableModel(cameras)
        return table_model

    def check_exit_status(self) -> bool:
        normal_exit = Js08Settings.get('normal_shutdown')
        Js08Settings.set('normal_shutdown', False)
        return normal_exit

    def update_cameras(self, cameras: list, update_target: bool = False) -> None:
        # Remove deleted cameras
        cam_id_in_db = [cam["_id"] for cam in self._model.read_cameras()]
        cam_id_in_arg = [cam["_id"] for cam in cameras]
        for cam_id in cam_id_in_db:
            if cam_id not in cam_id_in_arg:
                self._model.delete_camera(cam_id)
    
        # if `cameras` does not have 'targets' field, add an empty list for it.
        for cam in cameras:
            if 'targets' not in cam:
                cam['targets'] = []

        # Copy targets if `update_target` is False.
        if update_target == False:
            cam_in_db = self._model.read_cameras()
            for c_db in cam_in_db:
                for c_arg in cameras:
                    if c_arg['_id'] == c_db['_id']:
                        c_arg['targets'] = c_db['targets']
                        continue
        
        # if '_id' is empty, delete the field
        for cam in cameras:
            if not cam['_id']:
                del cam['_id']

        # Update existing camera or Insert new cameras
        for cam in cameras:
            self._model.upsert_camera(cam)

    @pyqtSlot()
    def close_process(self) -> None:
        Js08Settings.set('normal_shutdown', True)

    def get_attr(self) -> dict:
        attr_doc = self._model.read_attr()
        # attr_doc = None
        # if self._attr.count_documents({}):
        #     attr_doc = list(self._attr.find().sort("_id", -1).limit(1))[0]
        return attr_doc
    
    def insert_attr(self, model: dict) -> None:
        self._model.insert_attr(model)

    @pyqtSlot()
    def restore_defaults(self) -> None:
        Js08Settings.restore_defaults()

    @pyqtSlot(bool)
    def set_normal_shutdown(self) -> None:
         Js08Settings.set('normal_shutdown', True)

    def get_cameras(self) -> list:
        return self._model.read_cameras()


class Js08InferenceWorker(QObject):
    finished = pyqtSignal()
    
    def __init__(self, epoch: int, front_uri: str, rear_uri: str, front_decomposed_targets: list, rear_decomposed_targets: list) -> None:
        """
        Parameters:
            ctrl:
        """
        super().__init__()
        
        # TODO(Kyungwon): Put the model file into Qt Resource Collection.
        if getattr(sys, 'frozen', False):
            directory = sys._MEIPASS
        else:
            directory = os.path.dirname(__file__)

        self.epoch = epoch
        self.front_uri = front_uri
        self.rear_uri = rear_uri
        self.front_targets = front_decomposed_targets
        self.rear_targets = rear_decomposed_targets

        self.batch_size = Js08Settings.get('inference_batch_size')

        # Prepare model.
        model_path = os.path.join(directory, 'resources', 'js08_1636343249.onnx')
        providers = ['CPUExecutionProvider']
        self.session = ort.InferenceSession(model_path, providers=providers)

        # Prepare mask array.
        input_shape = self.session.get_inputs()[0].shape
        self.input_height = input_shape[1]
        self.input_width = input_shape[2]

    def grab_image(self, uri: str) -> QImage:
        """
        Parameters:
            uri: URI of a video stream
        """
        cap = cv2.VideoCapture(uri)
        ret, frame = cap.read()
        image = None
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        return image

    def save_image(self, dir: str, filename: str, image: QImage) -> None:
        os.makedirs(dir, exist_ok=True)
        path = QDir.cleanPath(os.path.join(dir, filename))
        image.save(path)

    def classify_image(self, image: np.ndarray) -> np.ndarray:
        """Discriminate the image.

        Return 1 if the model can discriminate the image, 0 otherwise.
        """
        input_data = image
        input_name = self.session.get_inputs()[0].name
        output_data = self.session.run(None, {input_name: input_data})
        tops = np.argmax(output_data, axis=-1)
        return np.squeeze(tops)

    def run(self):
        front_image = self.grab_image(self.front_uri)
        rear_image = self.grab_image(self.rear_uri)

        if front_image is None:
            print('DEBUG: Failed to capture the front video stream')
            self.finished.emit()
            return

        if rear_image is None:
            print('DEBUG: Failed to capture the rear video stream')
            self.finished.emit()
            return

        if Js08Settings.get('save_vista'):
            basepath = Js08Settings.get('image_base_path')
            now = QDateTime.fromSecsSinceEpoch(self.epoch)
            dir = os.path.join(basepath, 'vista', now.toString("yyyy-MM-dd"))
            filename = f'vista-front-{now.toString("yyyy-MM-dd-hh-mm")}.png'
            self.save_image(dir, filename, front_image)
            filename = f'vista-rear-{now.toString("yyyy-MM-dd-hh-mm")}.png'
            self.save_image(dir, filename, rear_image)
        
        # Discriminate the targets of front camera
        self.classify_batch(self.front_targets, front_image)

        # Discriminate the targets of rear camera
        self.classify_batch(self.rear_targets, rear_image)

        self.finished.emit()

    def classify_batch(self, targets: List[Js08SimpleTarget], vista: QImage):
        """Discriminate image batch

        Parameters:
            targets: List of Js08SimpleTarget
            vista: QImage
        """
        save_target_clip = Js08Settings.get('save_target_clip')
        if save_target_clip:
            basepath = Js08Settings.get('image_base_path')
            dir = os.path.join(basepath, 'target', str(self.epoch))
            os.makedirs(dir, exist_ok=True)
            masked_img_list = []

        padding_size = -len(targets) % self.batch_size
        result = np.zeros(len(targets) + padding_size)
        for i, target in enumerate(targets):
            if i % self.batch_size == 0:
                data = np.zeros(
                    (self.batch_size, self.input_height, self.input_width, 3), 
                    dtype=np.float32
                    )

            roi_image = target.clip_roi(vista)
            arr = target.img_to_arr(roi_image, self.input_width, self.input_height)
            masked_arr = arr * target.mask
            data[i % self.batch_size] = masked_arr

            if save_target_clip:
                masked_img = target.arr_to_img(masked_arr)
                masked_img_list.append(masked_img)

            if i % self.batch_size == self.batch_size - 1:
                result[i - self.batch_size + 1: i + 1] = self.classify_image(data)
            elif i == len(targets) - 1:
                chunk_size = len(targets) % self.batch_size
                result[i - chunk_size + 1:] = self.classify_image(data)

        for i, target in enumerate(targets):
            target.discernment = bool(result[i] == 1)
            if save_target_clip:
                postfix = 'pos' if target.discernment else 'neg'
                filename = f'{target.label}_{postfix}.png'
                self.save_image(dir, filename, masked_img_list[i])