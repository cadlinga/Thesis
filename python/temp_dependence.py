from numpy import linspace
import matplotlib.pyplot as plt
from matplotlib import cm


def d_from_T(temperature):
    d_0 = 2.87771 * 10**9
    d_1 = -4.6 * 10**-6
    d_2 = 1.067 * 10**-7
    d_3 = -9.325 * 10**-10
    d_4 = 1.739 * 10**-12
    d_5 = -1.838 * 10**-15
    T = temperature
    D = d_0 + d_1 * T + d_2 * T**2 + d_3 * T**3 + d_4 * T**4 + d_5 * T**5
    return D


T_array = linspace(0, 400, 20)
D_array = []
for T in T_array:
    D_array.append(d_from_T(T))

# plt.plot(T_array, D_array)
ax = plt.figure().add_subplot(projection="3d")
ax.plot(T_array, D_array, zs=50, zdir="z", label="curve in (x, y)")
ax.plot(T_array, D_array, zs=150, zdir="z", label="curve in (x, y)")
# plot_wireframe(T_array, D_array, D_array, rstride=10, cstride=10)
ax.view_init(elev=20.0, azim=-35, roll=0)
plt.show()
