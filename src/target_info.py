#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np

import cv2
import datetime
import time
import cal_ext_coef


def minprint(epoch, left_range, right_range, distance, cv_img):
    """A function that outputs pixels for calculating the dissipation coefficient in the specified areas"""
    # print("minprint 시작")
    # epoch = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
    cp_image = cv_img.copy()
    result = ()
    cnt = 1
    min_x = []
    min_y = []

    for upper_left, lower_right in zip(left_range, right_range):
        result = minrgb(upper_left, lower_right, cp_image)
        min_x.append(result[0])
        min_y.append(result[1])
        cnt += 1

    visibility = get_rgb(epoch, min_x, min_y, cp_image, distance)
    return visibility

def minrgb(upper_left, lower_right, cp_image):
    """Extracts the minimum RGB value of the dragged area"""

    up_y = min(upper_left[1], lower_right[1])
    down_y = max(upper_left[1], lower_right[1])

    left_x = min(upper_left[0], lower_right[0])
    right_x = max(upper_left[0], lower_right[0])

    test = cp_image[up_y:down_y, left_x:right_x, :]

    r = test[:, :, 0]
    g = test[:, :, 1]
    b = test[:, :, 2]

    r = np.clip(r, 0, 765)
    sum_rgb = r + g + b

    t_idx = np.where(sum_rgb == np.min(sum_rgb))
    
    # print("red : ", cp_image[t_idx[0][0] + up_y, t_idx[1][0] + left_x,0])
    # print("green : ", cp_image[t_idx[0][0] + up_y, t_idx[1][0] + left_x,1])
    # print("blue : ", cp_image[t_idx[0][0] + up_y, t_idx[1][0] + left_x,2])
    show_min_y = t_idx[0][0] + up_y
    show_min_x = t_idx[1][0] + left_x

    return (show_min_x, show_min_y)

def get_rgb(epoch: str, min_x, min_y, cp_image, distance):
    """Gets the RGB values ​​of the coordinates."""
    r_list = []
    g_list = []
    b_list = []

    for x, y in zip(min_x, min_y):

        r_list.append(cp_image[y, x, 0])
        g_list.append(cp_image[y, x, 1])
        b_list.append(cp_image[y, x, 2])
    
    print("red list : ", r_list)
    print("green list : ", g_list)
    print("blue list : ", b_list)

    visibility = save_rgb(r_list, g_list, b_list, epoch, distance)
    return visibility

def save_rgb(r_list, g_list, b_list, epoch, distance):
    """Save the rgb information for each target."""
    try:
        save_path = os.path.join(f"rgb/PNM_9030V")
        os.mkdir(save_path)

    except Exception as e:
        pass

    if r_list:
        
        r_list = list(map(int, r_list))
        g_list = list(map(int, g_list))
        b_list = list(map(int, b_list))       
        
        col = ["target_name", "r", "g", "b", "distance"]
        result = pd.DataFrame(columns=col)
        result["target_name"] = [f"target_{num}" for num in range(1, len(r_list) + 1)]
        result["r"] = r_list
        result["g"] = g_list
        result["b"] = b_list
        result["distance"] = distance
        result.to_csv(f"{save_path}/{epoch}.csv", mode="w", index=False)
        list1, list2, list3, select_color = cal_ext_coef.cal_curve(result)
        visibility = extinc_print(list1, list2, list3, select_color)
        print(result)
        print("Save rgb") 
    
    return visibility

def extinc_print(c1_list: list = [0, 0, 0], c2_list: list = [0, 0, 0], alp_list: list = [0, 0, 0], select_color: str = ""):
    """Select an appropriate value among visibility by wavelength."""
    g_ext = round(alp_list[1], 1)

    if select_color == "red" : 
        visibility = visibility_print(alp_list[0])
    elif select_color == "green" : 
        visibility = visibility_print(alp_list[1])
    else:
        visibility = visibility_print(alp_list[2])

    return visibility

def visibility_print(ext_g: float = 0.0):
    """Print the visibility"""
    vis_value = 0

    vis_value = (3.912/ext_g)
    if vis_value > 20:
        vis_value = 20
    elif vis_value < 0.01:
        vis_value = 0.01

    # self.data_storage(vis_value)
    vis_value_str = f"{vis_value:.3f}"
    return vis_value_str
        
def get_target(camera_name: str):
    """Retrieves target information of a specific camera."""

    save_path = os.path.join(f"target/{camera_name}")
    print("Get target information")
    if os.path.isfile(f"{save_path}/{camera_name}.csv"):
        target_df = pd.read_csv(f"{save_path}/{camera_name}.csv")
        target_name = target_df["target_name"].tolist()
        left_range = target_df["left_range"].tolist()
        left_range = str_to_tuple(left_range)
        right_range = target_df["right_range"].tolist()
        right_range = str_to_tuple(right_range)
        distance = target_df["distance"].tolist()
        return target_name, left_range, right_range, distance
    else:
        print("Target Information Not Found")
        return [], [], [], []

def str_to_tuple(before_list):
    """A function that converts the tuple list, which is the location information of the stored targets, 
    into a string and converts it back into a tuple form."""
    tuple_list = [i.split(',') for i in before_list]
    tuple_list = [(int(i[0][1:]), int(i[1][:-1])) for i in tuple_list]
    return tuple_list