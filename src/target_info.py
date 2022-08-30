#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

import os
import pandas as pd
import numpy as np
import cv2

from cal_ext_coef import Coef
from model import JS08Settings


class TargetInfo:

    def __init__(self):
        self.coef = Coef()

        self.list1, self.list2, self.list3, self.select_color = None, None, None, None

    def minprint(self, epoch, left_range, right_range, distance, cv_img, camera):
        """A function that outputs pixels for calculating the dissipation coefficient in the specified areas"""

        cp_image = cv_img.copy()
        # cv2.imwrite(f'test/{epoch}.png', cp_image)
        min_x = []
        min_y = []

        for upper_left, lower_right in zip(left_range, right_range):
            result = self.minrgb(upper_left, lower_right, cp_image)
            min_x.append(result[0])
            min_y.append(result[1])

        visibility = self.get_rgb(epoch, min_x, min_y, cp_image, distance, camera)

        if visibility is None:
            visibility = 0

        return visibility

    def minrgb(self, upper_left, lower_right, cp_image):
        """Extracts the minimum RGB value of the dragged area"""

        up_y = min(upper_left[1], lower_right[1])
        down_y = max(upper_left[1], lower_right[1])

        left_x = min(upper_left[0], lower_right[0])
        right_x = max(upper_left[0], lower_right[0])

        target = cp_image[up_y:down_y, left_x:right_x, :]

        r = target[:, :, 0]
        g = target[:, :, 1]
        b = target[:, :, 2]

        r = np.clip(r, 0, 765)
        sum_rgb = r + g + b

        t_idx = np.where(sum_rgb == np.min(sum_rgb))

        show_min_y = t_idx[0][0] + up_y
        show_min_x = t_idx[1][0] + left_x

        return show_min_x, show_min_y

    def get_rgb(self, epoch: str, min_x, min_y, cp_image, distance, camera):
        """Gets the RGB values of the coordinates."""

        r_list = []
        g_list = []
        b_list = []

        for x, y in zip(min_x, min_y):
            r_list.append(cp_image[y, x, 0])
            g_list.append(cp_image[y, x, 1])
            b_list.append(cp_image[y, x, 2])

        visibility = self.save_rgb(r_list, g_list, b_list, epoch, distance, camera)

        return visibility

    def save_rgb(self, r_list, g_list, b_list, epoch, distance, camera):
        """Save the rgb information for each target."""

        # save_path = os.path.join(f'rgb/{camera}/{epoch[:4]}/{epoch[4:8]}')
        save_path = os.path.join(f'{JS08Settings.get("rgb_csv_path")}/{camera}/{epoch[:4]}/{epoch[4:8]}')
        os.makedirs(save_path, exist_ok=True)

        if r_list:
            r_list = list(map(int, r_list))
            g_list = list(map(int, g_list))
            b_list = list(map(int, b_list))

            col = ['time', 'target_name', 'r', 'g', 'b', 'distance']
            result = pd.DataFrame(columns=col)
            result['target_name'] = [f'target_{num}' for num in range(1, len(r_list) + 1)]
            result['r'] = r_list
            result['g'] = g_list
            result['b'] = b_list
            result['distance'] = distance
            result.to_csv(f'{save_path}/{epoch}00.csv', mode='w', index=False)

            try:
                self.list1, self.list2, self.list3, self.select_color = self.coef.cal_curve(result)
            except TypeError:
                # list1, list2, list3, select_color = [0.01], [0.01], [0.01], 'red'
                pass

            visibility = self.extinc_print(self.list3, self.select_color)

            return visibility

    def extinc_print(self, alp_list: list, select_color: str = ''):
        """Select an appropriate value among visibility by wavelength."""
        visibility = 0

        if select_color == 'red':
            visibility = self.visibility_print(alp_list[0])
        elif select_color == 'green':
            visibility = self.visibility_print(alp_list[1])
        elif select_color == 'blue':
            visibility = self.visibility_print(alp_list[2])

        return visibility

    def visibility_print(self, ext_g: float=0.0):
        """Print the visibility"""

        vis_value = (3.912 / ext_g)
        if vis_value > 20:
            vis_value = 20
        elif vis_value <= 0.01:
            vis_value = 0.01

        vis_value_str = f'{vis_value:.3f}'

        return vis_value_str

    def get_target(self, camera_name: str):
        """Retrieves target information of a specific camera."""

        save_path = JS08Settings.get('target_csv_path')

        if os.path.isfile(f'{save_path}/{camera_name}/{camera_name}.csv'):
            target_df = pd.read_csv(f'{save_path}/{camera_name}/{camera_name}.csv')
            target_name = target_df['target_name'].tolist()
            left_range = self.str_to_tuple(target_df['left_range'].tolist())
            right_range = self.str_to_tuple(target_df['right_range'].tolist())
            distance = target_df['distance'].tolist()
            azimuth = target_df['azimuth'].tolist()

            return target_name, left_range, right_range, distance, azimuth

        else:
            return [], [], [], [], []

    def get_target_from_azimuth(self, camera_name: str, azimuth: str):
        """Retrieves target information from azimuth of a specific camera"""

        save_path = JS08Settings.get('target_csv_path')

        if os.path.isfile(f'{save_path}/{camera_name}/{camera_name}.csv'):
            target_df = pd.read_csv(f'{save_path}/{camera_name}/{camera_name}.csv')
            azi_target = target_df.loc[(target_df['azimuth'] == f'{azimuth}'), :]

            target_name = azi_target['target_name'].tolist()
            left_range = self.str_to_tuple(azi_target['left_range'].tolist())
            right_range = self.str_to_tuple(azi_target['right_range'].tolist())
            distance = azi_target['distance'].tolist()

            return target_name, left_range, right_range, distance, azimuth

        else:

            return [], [], [], [], []

    def str_to_tuple(self, before_list):
        """A function that converts the tuple list, which is the location information of the stored targets,
        into a string and converts it back into a tuple form."""
        tuple_list = [i.split(',') for i in before_list]
        tuple_list = [(int(i[0][1:]), int(i[1][:-1])) for i in tuple_list]
        return tuple_list


if __name__ == '__main__':

    target_info = TargetInfo()
    front_target_name_W, front_left_range_W, front_right_range_W, front_distance_W, front_azimuth_W = \
        target_info.get_target_from_azimuth(JS08Settings.get('front_camera_name'), 'W')

    print(front_target_name_W)
    print(front_left_range_W)
    print(front_right_range_W)
    print(front_distance_W)
    print(front_azimuth_W)
