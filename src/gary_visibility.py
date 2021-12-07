import itertools
import os

import numpy as np
import pandas as pd

import scipy
from scipy.optimize import curve_fit
import matplotlib
import matplotlib.pyplot as plt


def minprint(self):
        """지정한 구역들에서 소산계수 산출용 픽셀을 출력하는 함수"""
        result = ()
        cnt = 1
        min_x = []
        min_y = []

        for upper_left, lower_right in zip(left_range, right_range):
            result = minrgb(upper_left, lower_right)
            print(f"target{cnt}의 소산계수 검출용 픽셀위치 =  ", result)
            min_x.append(result[0])
            min_y.append(result[1])
            cnt += 1

        get_rgb(epoch)

        curved_thread = CurvedThread(camera_name, epoch)
        curved_thread.update_extinc_signal.connect(extinc_print)
        curved_thread.run()

        list_test()

        graph_dir = os.path.join(f"extinction/{camera_name}")
def minrgb(self, upper_left, lower_right):
        """드래그한 영역의 RGB 최솟값을 추출한다"""

        up_y = min(upper_left[1], lower_right[1])
        down_y = max(upper_left[1], lower_right[1])

        left_x = min(upper_left[0], lower_right[0])
        right_x = max(upper_left[0], lower_right[0])

        test = cp_image[up_y:down_y, left_x:right_x, :]

        # 드래그한 영역의 RGB 값을 각각 추출한다.
        # r = test[:, :]
        # g = test[:, :, 1]
        # b = test[:, :, 2]

        # RGB값을 각 위치별로 모두 더한다.
        # RGB 최댓값이 255로 정해져있어 값을 초과하면 0부터 시작된다. numpy의 clip 함수를 이용해 array의 최댓값을 수정한다.
        # r = np.clip(r, 0, 765)
        # sum_rgb = r + g + b

        # RGB 값을 합한 뒤 가장 최솟값의 index를 추출한다.
        t_idx = np.where(test == np.min(test))

        show_min_y = t_idx[0][0] + up_y
        show_min_x = t_idx[1][0] + left_x

        return (show_min_x, show_min_y)

def get_rgb(self, epoch: str):
    r_list = []
    g_list = []
    b_list = []

    for x, y in zip(min_x, min_y):

        r_list.append(cp_image[y, x, 0])
        g_list.append(cp_image[y, x, 1])
        b_list.append(cp_image[y, x, 2])

        print("red : ", cp_image[y, x, 0])
        print("green : ", cp_image[y, x, 1])
        print("blue: ", cp_image[y, x, 2])


    save_rgb(r_list, g_list, b_list, epoch)

def save_rgb(self, r_list, g_list, b_list, epoch):
    """Save the rgb information for each target."""
    try:
        save_path = os.path.join(f"rgb/{camera_name}")
        os.mkdir(save_path)

    except Exception as e:
        pass

    if r_list:
        r_list = list(map(int, r_list))
        g_list = list(map(int, g_list))
        b_list = list(map(int, b_list))
        print(b_list)
        
        col = ["target_name", "r", "g", "b", "distance"]
        result = pd.DataFrame(columns=col)
        result["target_name"] = target_name
        result["r"] = r_list
        result["g"] = g_list
        result["b"] = b_list
        result["distance"] = distance
        print(result.head(10))
        result.to_csv(f"{save_path}/{epoch}.csv", mode="w", index=False)