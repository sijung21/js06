import os
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtGui, QtCore

class CurvedThread(QtCore.QThread):
    # update_extinc_signal = QtCore.pyqtSignal(float, float)
    update_extinc_signal = QtCore.pyqtSignal(list, list, list)

    def __init__(self, cam_name: str = "", epoch: str = ""):
        super().__init__()
        self.curved_flag = True
        self.cam_name = cam_name
        self.hanhwa_dist = []
        self.hanhwa_x = []
        self.hanhwa_r = []
        self.hanhwa_g = []
        self.hanhwa_b = []
        self.epoch = epoch
        self.rgbsavedir = os.path.join(f"rgb/{self.cam_name}")
        self.extsavedir = os.path.join(f"extinction/{self.cam_name}")
    def run(self):

        hanhwa = pd.read_csv(f"{self.rgbsavedir}/{self.epoch}.csv")
        hanhwa = hanhwa.sort_values(by=['distance'])
        self.hanhwa_dist = hanhwa[['distance']].squeeze().to_numpy()
        print(self.hanhwa_dist[0], ", ", self.hanhwa_dist[-1])
        self.hanhwa_x = np.linspace(self.hanhwa_dist[0], self.hanhwa_dist[-1], 100, endpoint=True)
        self.hanhwa_x.sort()
        print(self.hanhwa_x)
        self.hanhwa_r = hanhwa[['r']].squeeze().to_numpy()
        self.hanhwa_g = hanhwa[['g']].squeeze().to_numpy()
        self.hanhwa_b = hanhwa[['b']].squeeze().to_numpy()
                 
        r1_init = self.hanhwa_r[0] * 0.7
        g1_init = self.hanhwa_g[0] * 0.7
        b1_init = self.hanhwa_b[0] * 0.7

        r2_init = self.hanhwa_r[-1] * 1.3
        g2_init = self.hanhwa_g[-1] * 1.3
        b2_init = self.hanhwa_b[-1] * 1.3
        
        r_ext_init = [r1_init, r2_init, 1]
        g_ext_init = [g1_init, g2_init, 1]
        b_ext_init = [b1_init, b2_init, 1]
        try:
            hanhwa_opt_r, hanhwa_cov_r = curve_fit(self.func, self.hanhwa_dist, self.hanhwa_r, p0=r_ext_init, maxfev=5000)
            hanhwa_opt_g, hanhwa_cov_g = curve_fit(self.func, self.hanhwa_dist, self.hanhwa_g, p0=g_ext_init, maxfev=5000)
            hanhwa_opt_b, hanhwa_cov_b = curve_fit(self.func, self.hanhwa_dist, self.hanhwa_b, p0=b_ext_init, maxfev=5000)

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

        self.print_result(hanhwa_opt_r, hanhwa_opt_g, hanhwa_opt_b, hanhwa_err_r, hanhwa_err_g, hanhwa_err_b)

        print(f"Red channel: {self.extcoeff_to_vis(hanhwa_opt_r[2], hanhwa_err_r[2], 3)} km")
        print(f"Green channel: {self.extcoeff_to_vis(hanhwa_opt_g[2], hanhwa_err_g[2], 3)} km")
        print(f"Blue channel: {self.extcoeff_to_vis(hanhwa_opt_b[2], hanhwa_err_b[2], 3)} km")

        self.update_extinc_signal.emit(list1, list2, list3)

        try:
            os.mkdir(self.extsavedir)
        except Exception as e:
            pass

        plt.figure(figsize=(13, 8))
        plt.plot(self.hanhwa_dist, self.hanhwa_r, '.', c='red')
        plt.plot(self.hanhwa_dist, self.hanhwa_g, '.', c='green')
        plt.plot(self.hanhwa_dist, self.hanhwa_b, '.', c='blue')
        plt.plot(self.hanhwa_x, self.func(self.hanhwa_x, *hanhwa_opt_r), label='Red', c='red')
        plt.plot(self.hanhwa_x, self.func(self.hanhwa_x, *hanhwa_opt_g), label='Green', c='green')
        plt.plot(self.hanhwa_x, self.func(self.hanhwa_x, *hanhwa_opt_b), label='Blue', c='blue')
        plt.xlabel('Distance (km)')
        plt.ylabel('Amplitude')
        plt.legend(prop={'size': 20})
        plt.title(self.cam_name)
        plt.grid(True)
        plt.savefig(f'{self.extsavedir}/{self.epoch}.png', dpi=300)

    def func(self, x, c1, c2, a):
        return c2 + (c1 - c2) * np.exp(-a * x)

    def print_result(self, opt_r, opt_g, opt_b, err_r, err_g, err_b):
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

    def extcoeff_to_vis(self, optimal, error, coeff=3.291):
        return coeff / (optimal + np.array((1, 0, -1)) * error)






