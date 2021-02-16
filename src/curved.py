import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def func(x, c1, c2, a):
    return c2 + (c1 - c2) * np.exp(-a * x)

noir_opt_r, noir_cov_r = curve_fit(func, noir_dist, noir_r)
noir_opt_g, noir_cov_g = curve_fit(func, noir_dist, noir_g)
noir_opt_b, noir_cov_b = curve_fit(func, noir_dist, noir_b)

noir_err_r = np.sqrt(np.diag(noir_cov_r))
noir_err_g = np.sqrt(np.diag(noir_cov_g))
noir_err_b = np.sqrt(np.diag(noir_cov_b))

plt.figure(figsize=(13,8))
plt.plot(noir_dist, noir_r, '.', c='red')
plt.plot(noir_dist, noir_g, '.', c='green')
plt.plot(noir_dist, noir_b, '.', c='blue')
plt.plot(noir_x, func(noir_x, *noir_opt_r), label='Red', c='red')
plt.plot(noir_x, func(noir_x, *noir_opt_g), label='Green', c='green')
plt.plot(noir_x, func(noir_x, *noir_opt_b), label='Blue', c='blue')
plt.xlabel('Distance (km)')
plt.ylabel('Amplitude')
plt.legend(prop={'size': 20})
plt.title(title)
plt.grid(True)

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

print_result(noir_opt_r, noir_opt_g, noir_opt_b, noir_err_r, noir_err_g, noir_err_b)

def extcoeff_to_vis(optimal, error, coeff=3.291):
  return coeff / (optimal + np.array((1, 0, -1)) * error)

print(f"Red channel: {extcoeff_to_vis(noir_opt_r[2], noir_err_r[2], 3)} km")
print(f"Green channel: {extcoeff_to_vis(noir_opt_g[2], noir_err_g[2], 3)} km")
print(f"Blue channel: {extcoeff_to_vis(noir_opt_b[2], noir_err_b[2], 3)} km")