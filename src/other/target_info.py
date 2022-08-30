#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np

import cal_ext_coef
from model import JS08Settings


def minprint(epoch, left_range, right_range, distance, cv_img, camera):
    """A function that outputs pixels for calculating the dissipation coefficient in the specified areas"""

    cp_image = cv_img.copy()
    min_x = []
    min_y = []

    for upper_left, lower_right in zip(left_range, right_range):
        result = minrgb(upper_left, lower_right, cp_image)
        min_x.append(result[0])
        min_y.append(result[1])

    visibility = get_rgb(epoch, min_x, min_y, cp_image, distance, camera)

    # print(f'minprint visibility: {visibility}')
    return visibility


def minrgb(upper_left, lower_right, cp_image):
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


def get_rgb(epoch: str, min_x, min_y, cp_image, distance, camera):
    """Gets the RGB values of the coordinates."""

    r_list = []
    g_list = []
    b_list = []

    for x, y in zip(min_x, min_y):
        r_list.append(cp_image[y, x, 0])
        g_list.append(cp_image[y, x, 1])
        b_list.append(cp_image[y, x, 2])

    visibility = save_rgb(r_list, g_list, b_list, epoch, distance, camera)

    # print(f'get_rgb visibility: {visibility}')
    return visibility


def save_rgb(r_list, g_list, b_list, epoch, distance, camera):
    """Save the rgb information for each target."""

    save_path = os.path.join(f'rgb/{camera}')
    os.makedirs(save_path, exist_ok=True)

    try:
        if r_list:
            r_list = list(map(int, r_list))
            g_list = list(map(int, g_list))
            b_list = list(map(int, b_list))

            col = ['target_name', 'r', 'g', 'b', 'distance']
            result = pd.DataFrame(columns=col)
            result['target_name'] = [f'target_{num}' for num in range(1, len(r_list) + 1)]
            result['r'] = r_list
            result['g'] = g_list
            result['b'] = b_list
            result['distance'] = distance
            result.to_csv(f'{save_path}/{epoch}.csv', mode='w', index=False)
            list1, list2, list3, select_color = cal_ext_coef.cal_curve(result)

            # visibility = extinc_print(list1, list2, list3, select_color)
            visibility = extinc_print(list3, select_color)

            # print(f'save_rgb visibility: {visibility}')
            return visibility

    except TypeError:
        pass


def extinc_print(alp_list: list, select_color: str = ""):
    """Select an appropriate value among visibility by wavelength."""
    visibility = 0

    if select_color == 'red':
        visibility = visibility_print(alp_list[0])
    elif select_color == 'green':
        visibility = visibility_print(alp_list[1])
    elif select_color == 'blue':
        visibility = visibility_print(alp_list[2])

    # print(f'extinc_print visibility: {visibility}')
    return visibility


def visibility_print(ext_g: float = 0.0):
    """Print the visibility"""

    vis_value = (3.912 / ext_g)
    if vis_value > 20:
        vis_value = 20
    elif vis_value <= 0.01:
        vis_value = 0.01

    vis_value_str = f'{vis_value:.3f}'

    return vis_value_str


def get_target(camera_name: str):
    """Retrieves target information of a specific camera."""

    save_path = JS08Settings.get('target_csv_path')

    if os.path.isfile(f'{save_path}/{camera_name}/{camera_name}.csv'):
        target_df = pd.read_csv(f'{save_path}/{camera_name}/{camera_name}.csv')
        target_name = target_df['target_name'].tolist()
        left_range = str_to_tuple(target_df['left_range'].tolist())
        right_range = str_to_tuple(target_df['right_range'].tolist())
        distance = target_df['distance'].tolist()
        azimuth = target_df['azimuth'].tolist()

        return target_name, left_range, right_range, distance, azimuth

    else:
        return [], [], [], [], []


def get_target_from_azimuth(camera_name: str, azimuth: str):
    """Retrieves target information from azimuth of a specific camera"""

    global target_name, left_range, right_range, distance
    save_path = JS08Settings.get('target_csv_path')

    if os.path.isfile(f'{save_path}/{camera_name}/{camera_name}.csv'):
        target_df = pd.read_csv(f'{save_path}/{camera_name}/{camera_name}.csv')
        azi_target = target_df.loc[(target_df['azimuth'] == f'{azimuth}'), :]

        target_name = azi_target['target_name'].tolist()
        left_range = str_to_tuple(azi_target['left_range'].tolist())
        right_range = str_to_tuple(azi_target['right_range'].tolist())
        distance = azi_target['distance'].tolist()

        return target_name, left_range, right_range, distance, azimuth

    else:


        return [], [], [], [], []

    # if select_data == 'target_name':
    #     return target_name
    #
    # elif select_data == 'left_range':
    #     return left_range
    #
    # elif select_data == 'right_range':
    #     return right_range
    #
    # elif select_data == 'distance':
    #     return distance


def str_to_tuple(before_list):
    """A function that converts the tuple list, which is the location information of the stored targets,
    into a string and converts it back into a tuple form."""
    tuple_list = [i.split(',') for i in before_list]
    tuple_list = [(int(i[0][1:]), int(i[1][:-1])) for i in tuple_list]
    return tuple_list


if __name__ == '__main__':

    front_target_name_W, front_left_range_W, front_right_range_W, front_distance_W, front_azimuth_W = \
        get_target_from_azimuth('PNM_9031RV_front', 'W')

    print(front_target_name_W)
    print(front_left_range_W)
    print(front_right_range_W)
    print(front_distance_W)
    print(front_azimuth_W)
