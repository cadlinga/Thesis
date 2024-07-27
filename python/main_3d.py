import matplotlib.pyplot as plt

from sympy import Matrix
from numpy import cos, sin, sqrt, exp, linspace, pi, absolute, arccos

# DEFAULT VALUES
B_array = linspace(0, 0.05, 20)
B = 0.05
E = 0
D = 2.87 * 10**9
theta = 0  # Radians
phi = 0  # Radians


def makeMatrix(B=B, E=E, D=D, theta=theta, phi=phi) -> Matrix:
    M = Matrix(
        [
            [D + B * cos(theta), (B / sqrt(2)) *
             exp(-1j * phi) * sin(theta), E],
            [
                (B / sqrt(2)) * exp(1j * phi) * sin(theta),
                0,
                (B / sqrt(2)) * exp(-1j * phi) * sin(theta),
            ],
            [E, (B / sqrt(2)) * exp(1j * phi) *
             sin(theta), D - (B * cos(theta))],
        ]
    )
    # M = Matrix(
    #     [
    #         [D / 3 + B * cos(theta), (B / sqrt(2)) * sin(theta), 0],
    #         [
    #             (B / sqrt(2)) * sin(theta),
    #             -2 * D / 3,
    #             (B / sqrt(2)) * sin(theta),
    #         ],
    #         [0, (B / sqrt(2)) * sin(theta), D / 3 - (B * cos(theta))],
    #     ]
    # )
    return M


def evals(B=B, E=E, D=D, theta=theta, phi=phi) -> list:
    M = makeMatrix(B=B, E=E, D=D, theta=theta, phi=phi)
    return absolute(list(M.eigenvals().keys()))


def addToPlot(
    ax, zs, label, colour, opacity=0.4, B_array=B_array, E=E, D=D, theta=theta, phi=phi
):
    y_array = []
    y_array.append([])
    y_array.append([])
    # y_array.append([])
    x_array = []
    # for B in B_array:
    #     es = evals(B=B, E=E, D=D, theta=theta, phi=phi)
    #     es = [num for num in es if abs(num) >= 10**7]
    #     x_array.append(B)
    #
    #     for count, e in enumerate(es):
    #         y_array[count].append(abs(e))
    #         print(count)
    #
    #     y_array[2].append(D)
    for B in B_array:
        es = sorted(evals(B=B, E=E, D=D, theta=theta, phi=phi))
        if len(es) == 2:
            es.append(es[1])

        # es = [num for num in es if abs(num) >= 10**7]
        x_array.append(B)
        y_array[0].append(abs(es[2] - es[0]))

        y_array[1].append(abs(es[1] - es[0]))
        # for count, e in enumerate(es):
        # y_array[count].append(abs(e))

    # ax.plot(T_array, D_array, zs=50, zdir="z", label="curve in (x, y)")
    # plt.plot(x_array, y_array[0], label=label, color=colour, alpha=opacity)
    # plt.plot(x_array, y_array[1], label=label, color=colour, alpha=opacity)
    ax.plot(
        x_array, y_array[0], zs=zs, zdir="x", label=label, color=colour, alpha=opacity
    )
    ax.plot(
        x_array, y_array[1], zs=zs, zdir="x", label=label, color=colour, alpha=opacity
    )
    # plt.plot(x_array, y_array[2])


# plt.xlabel("$B_0$")
# plt.ylabel("Eigenvalues of $H_{NV}$")


def millerAngle(miller_1, miller_2):
    return arccos(
        [
            (
                (miller_1[0] * miller_2[0])
                + (miller_1[1] * miller_2[1])
                + (miller_1[2] * miller_2[2])
            )
            / sqrt(
                (miller_1[0] ** 2 + miller_1[1] ** 2 + miller_1[2] ** 2)
                * (miller_2[0] ** 2 + miller_2[1] ** 2 + miller_2[2] ** 2)
            )
        ]
    )[0]


applied_B_miller = (0, 0, 1)

defect_axis = (1, 1, 1)
defect_2 = (-1, 1, 1)
defect_3 = (1, -1, 1)
defect_4 = (1, 1, -1)

millerAngle(applied_B_miller, defect_axis)


ax = plt.figure().add_subplot(projection="3d")


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


T_array = linspace(0, 400, 5)

for T in T_array:
    addToPlot(
        ax,
        zs=T,
        label="Defect 1 $(111)$ at " + str(T) + "K",
        colour="blue",
        opacity=0.5,
        D=d_from_T(T),
        E=0,
        theta=millerAngle(applied_B_miller, defect_axis),
    )

T_array = linspace(0, 400, 20)
D_array = []
for T in T_array:
    D_array.append(d_from_T(T))

ax.plot(T_array, D_array, zs=0, zdir="y", label="curve in (x, y)")


# addToPlot(
#     label="Defect 2 $(\\overline{1} 11)$",
#     colour="purple",
#     opacity=0.3,
#     E=0,
#     theta=millerAngle(applied_B_miller, defect_2),
# )
#
#
# addToPlot(
#     label="Defect 3 $(1 \\overline{1} 1)$",
#     colour="green",
#     opacity=0.3,
#     E=0,
#     theta=millerAngle(applied_B_miller, defect_3),
# )
#
# addToPlot(
#     label="Defect 4 $(11\\overline{1})$",
#     colour="red",
#     opacity=0.3,
#     E=0,
#     theta=millerAngle(applied_B_miller, defect_4),
# )
# # Generic Results
# addToPlot(label="$E= 0, \\theta = 0$", colour="black", opacity=1, E=0, theta=0)
# addToPlot(
#     label="$E= 0, \\theta = \\pi/8$", colour="blue", opacity=0.5, E=0, theta=pi / 8
# )
# addToPlot(label="$E= 0.005, \\theta = 0$",
#           colour="orange", opacity=0.5, E=0.005)
# addToPlot(label="$E= 0.010, \\theta = 0$",
#           colour="Purple", opacity=0.5, E=0.010)
# addToPlot(
#     label="$E= 0, \\theta = \\pi /3$", colour="green", opacity=0.5, E=0, theta=pi / 3
# )
#

# Diamond Results with B aligned to suface of cubic crystal
# addToPlot(label="$E= 0, \\theta = 0.927$",
#           colour="blue", opacity=0.8, E=0, theta=0.927)
# addToPlot(label="$E= 0, \\theta = 2.214$",
#           colour="blue", opacity=0.8, E=0, theta=2.214)
#
# Diamond results with B aligned to [210] (to generate 4 different angles)

# addToPlot(label="$E= 0, \\theta = 0.68$",
#           colour="blue", opacity=0.5, E=0, theta=0.68)
#
# addToPlot(label="$E= 0, \\theta = 1.83$",
#           colour="blue", opacity=0.5, theta=1.83)
#
# addToPlot(label="$E= 0, \\theta = 1.31$",
#           colour="blue", opacity=0.5, E=0, theta=1.31)
#
# addToPlot(label="Base", colour="black", opacity=1, E=0, theta=0.927)
# addToPlot(label="Base", colour="black", opacity=1, E=0, theta=5.355)
# addToPlot(label="Base", colour="black", opacity=1, E=0, theta=2.214)
# addToPlot(label="Base", colour="black", opacity=1, E=0, theta=4.069)
# addToPlot(label="Base", colour="black", opacity=1, E=0, theta=pi / 4)
# addToPlot(label="Base Lower D", colour="black",
# opacity=1, D=2.6 * 10**9, theta=0)
# addToPlot(label="Base, $E=50$", colour="green", E=5 * 10**6, theta=0)
# addToPlot(label="Base, $E=50$", colour="green", E=5 * 10**6, theta=pi * 0.4)
# addToPlot(label="Base, $E=500$", colour="blue", E=9 * 10**6, theta=0)

#
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.title("$B_0$ aligned with " + "".join(map(str, applied_B_miller)))
plt.xlim(left=0)
ax.set_xlabel("Temp ($K$)")
ax.set_ylabel("$B_0$")
ax.set_zlabel("")
plt.show()
