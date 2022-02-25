import itertools
import os

import numpy as np
import pandas as pd

import scipy
from scipy.optimize import curve_fit

curved_flag = True
# cam_name = cam_name
hanhwa_dist = []
hanhwa_x = []
hanhwa_r = []
hanhwa_g = []
hanhwa_b = []

def select_max_rgb(r, g, b):

    select_color = ""
    c_list = [r, g, b]

    c_index = c_list.index(max(c_list))

    if c_index == 0:
        select_color = "red"
    elif c_index == 1:
        select_color = "green"
    else :
        select_color = "blue"
        
    select_color = "green"
    return select_color

def cal_curve(hanhwa: pd.DataFrame):
    # hanhwa = pd.read_csv(f"{rgbsavedir}/{epoch}.csv")
    print(hanhwa)
    hanhwa = hanhwa.sort_values(by=['distance'])
    hanhwa_dist = hanhwa[['distance']].squeeze().to_numpy()
    hanhwa_x = np.linspace(hanhwa_dist[0], hanhwa_dist[-1], 100, endpoint=True)
    hanhwa_x.sort()
    hanhwa_r = hanhwa[['r']].squeeze().to_numpy()
    hanhwa_g = hanhwa[['g']].squeeze().to_numpy()
    hanhwa_b = hanhwa[['b']].squeeze().to_numpy()
    
    print("오리지날 green", hanhwa_g)
    # hanhwa_g = hanhwa_g[:-1]
    
    # hanhwa_g = np.append(hanhwa_g, np.array([160]))
    print("소산계수 산출용 green 리스트 :  ", hanhwa_g)

    r1_init = hanhwa_r[0] * 0.7
    g1_init = hanhwa_g[0] * 0.7
    b1_init = hanhwa_b[0] * 0.7

    r2_init = hanhwa_r[-1] * 1.3
    g2_init = hanhwa_g[-1] * 1.3
    # g2_init = 160 * 1.3
    b2_init = hanhwa_b[-1] * 1.3
    
    select_color = select_max_rgb(r2_init, g2_init, b2_init)
    
    r_ext_init = [r1_init, r2_init, 1]
    g_ext_init = [g1_init, g2_init, 1]
    b_ext_init = [b1_init, b2_init, 1]

    try:

        hanhwa_opt_r, hanhwa_cov_r = curve_fit(func, hanhwa_dist, hanhwa_r, p0=r_ext_init, maxfev=5000)
        hanhwa_opt_g, hanhwa_cov_g = curve_fit(func, hanhwa_dist, hanhwa_g, p0=g_ext_init, maxfev=5000)
        hanhwa_opt_b, hanhwa_cov_b = curve_fit(func, hanhwa_dist, hanhwa_b, p0=b_ext_init, maxfev=5000)

    except Exception as e:
        print("error msg: ", e)
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

    hanhwa_err_r = np.sqrt(np.diag(hanhwa_cov_r))
    hanhwa_err_g = np.sqrt(np.diag(hanhwa_cov_g))
    hanhwa_err_b = np.sqrt(np.diag(hanhwa_cov_b))

    print_result(hanhwa_opt_r, hanhwa_opt_g, hanhwa_opt_b, hanhwa_err_r, hanhwa_err_g, hanhwa_err_b)

    print(f"Red channel: {extcoeff_to_vis(hanhwa_opt_r[2], hanhwa_err_r[2], 3)} km")
    print(f"Green channel: {extcoeff_to_vis(hanhwa_opt_g[2], hanhwa_err_g[2], 3)} km")
    print(f"Blue channel: {extcoeff_to_vis(hanhwa_opt_b[2], hanhwa_err_b[2], 3)} km")

    return list1, list2, list3, select_color
    # update_extinc_signal.emit(list1, list2, list3, select_color)

    try:
        os.mkdir(extsavedir)
    except Exception as e:
        pass

# @staticmethod
def func(x, c1, c2, a):
    return c2 + (c1 - c2) * np.exp(-a * x)

def print_result(opt_r, opt_g, opt_b, err_r, err_g, err_b):
    print(f"Red channel: (",
            f"C1: {opt_r[0]:.2f} ± {err_r[0]:.2f}, ",
            f"C2: {opt_r[1]:.2f} ± {err_r[1]:.2f}, ",
            f"alpha: {opt_r[2]:.2f} ± {err_r[2]:.2f})")
    print(f"Green channel: (",
            f"C1: {opt_g[0]:.2f} ± {err_g[0]:.2f}, ",
            f"C2: {opt_g[1]:.2f} ± {err_g[1]:.2f}, ",
            f"alpha: {opt_g[2]:.2f} ± {err_g[2]:.2f})")
    print(f"Blue channel: (",
            f"C1: {opt_b[0]:.2f} ± {err_b[0]:.2f}, ",
            f"C2: {opt_b[1]:.2f} ± {err_b[1]:.2f}, ",
            f"alpha: {opt_b[2]:.2f} ± {err_b[2]:.2f})")

def extcoeff_to_vis(optimal, error, coeff=3.912):
    return coeff / (optimal + np.array((1, 0, -1)) * error)