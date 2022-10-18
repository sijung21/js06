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
from model import JS08Settings


class Coef:

    def __init__(self):
        self.hanhwa_dist = []
        self.hanhwa_x = []
        self.hanhwa_r = []
        self.hanhwa_g = []
        self.hanhwa_b = []

    def select_max_rgb(self, r, g, b):
        c_list = [r, g, b]
        c_index = c_list.index(max(c_list))

        if c_index == 0:
            select_color = 'red'
        elif c_index == 1:
            select_color = 'green'
        else:
            select_color = 'blue'

        return select_color

    def cal_curve(self, hanhwa: pd.DataFrame):
        hanhwa = hanhwa.sort_values(by=['distance'])
        self.hanhwa_dist = hanhwa[['distance']].squeeze().to_numpy()
        self.hanhwa_x = np.linspace(self.hanhwa_dist[0], self.hanhwa_dist[-1], 100, endpoint=True)
        self.hanhwa_x.sort()
        self.hanhwa_r = hanhwa[['r']].squeeze().to_numpy()
        self.hanhwa_g = hanhwa[['g']].squeeze().to_numpy()
        self.hanhwa_b = hanhwa[['b']].squeeze().to_numpy()

        r1_init = self.hanhwa_r[0] * 0.7
        g1_init = self.hanhwa_g[0] * 0.7

        b1_init = self.hanhwa_b[0] * 0.7
        r2_init = self.hanhwa_r[-1] * 1.3
        g2_init = self.hanhwa_g[-1] * 1.3
        b2_init = self.hanhwa_b[-1] * 1.3

        select_color = self.select_max_rgb(r2_init, g2_init, b2_init)

        r_ext_init = [r1_init, r2_init, 1]
        g_ext_init = [g1_init, g2_init, 1]
        b_ext_init = [b1_init, b2_init, 1]

        try:
            hanhwa_opt_r, hanhwa_cov_r = curve_fit(self.func, self.hanhwa_dist, self.hanhwa_r, p0=r_ext_init, maxfev=5000)
            hanhwa_opt_g, hanhwa_cov_g = curve_fit(self.func, self.hanhwa_dist, self.hanhwa_g, p0=g_ext_init, maxfev=5000)
            hanhwa_opt_b, hanhwa_cov_b = curve_fit(self.func, self.hanhwa_dist, self.hanhwa_b, p0=b_ext_init, maxfev=5000)
            JS08Settings.set('maxfev_flag', False)

        except RuntimeError:
            JS08Settings.set('maxfev_flag', True)
            JS08Settings.set('maxfev_count', JS08Settings.get('maxfev_count') + 1)
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

    def func(self, x, c1, c2, a):
        return c2 + (c1 - c2) * np.exp(-a * x)
