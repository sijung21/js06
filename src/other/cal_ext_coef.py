#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

import itertools
import os

import time
import numpy as np
import pandas as pd
import traceback

from scipy.optimize import curve_fit

curved_flag = True
hanhwa_dist = []
hanhwa_x = []
hanhwa_r = []
hanhwa_g = []
hanhwa_b = []


def select_max_rgb(r, g, b):
    c_list = [r, g, b]

    c_index = c_list.index(max(c_list))

    if c_index == 0:
        select_color = 'red'
    elif c_index == 1:
        select_color = 'green'
    else:
        select_color = 'blue'

    return select_color


def cal_curve(hanhwa: pd.DataFrame):
    hanhwa = hanhwa.sort_values(by=['distance'])
    hanhwa_dist = hanhwa[['distance']].squeeze().to_numpy()
    hanhwa_x = np.linspace(hanhwa_dist[0], hanhwa_dist[-1], 100, endpoint=True)
    hanhwa_x.sort()
    hanhwa_r = hanhwa[['r']].squeeze().to_numpy()
    hanhwa_g = hanhwa[['g']].squeeze().to_numpy()
    hanhwa_b = hanhwa[['b']].squeeze().to_numpy()

    r1_init = hanhwa_r[0] * 0.7
    g1_init = hanhwa_g[0] * 0.7

    b1_init = hanhwa_b[0] * 0.7
    r2_init = hanhwa_r[-1] * 1.3
    g2_init = hanhwa_g[-1] * 1.3
    b2_init = hanhwa_b[-1] * 1.3

    select_color = select_max_rgb(r2_init, g2_init, b2_init)

    r_ext_init = [r1_init, r2_init, 1]
    g_ext_init = [g1_init, g2_init, 1]
    b_ext_init = [b1_init, b2_init, 1]

    try:
        hanhwa_opt_r, hanhwa_cov_r = curve_fit(func, hanhwa_dist, hanhwa_r, p0=r_ext_init, maxfev=5000)
        hanhwa_opt_g, hanhwa_cov_g = curve_fit(func, hanhwa_dist, hanhwa_g, p0=g_ext_init, maxfev=5000)
        hanhwa_opt_b, hanhwa_cov_b = curve_fit(func, hanhwa_dist, hanhwa_b, p0=b_ext_init, maxfev=5000)

    except RuntimeError:
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} - {traceback.format_exc()}')
        return

    list1 = []
    list2 = []
    list3 = []

    list1.append(hanhwa_opt_r[0])
    list1.append(hanhwa_opt_g[0])
    list1.append(hanhwa_opt_b[0])

    list2.append(hanhwa_opt_r[1])
    list2.append(hanhwa_opt_g[1])
    list2.append(hanhwa_opt_b[1])

    list3.append(hanhwa_opt_r[2])
    list3.append(hanhwa_opt_g[2])
    list3.append(hanhwa_opt_b[2])

    return list1, list2, list3, select_color


def func(x, c1, c2, a):
    return c2 + (c1 - c2) * np.exp(-a * x)
