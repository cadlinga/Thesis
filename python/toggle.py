import inquirer
from defect import Defect
from numpy import absolute, linspace

import matplotlib.pyplot as plt
from matplotlib import cm

questions = [
    inquirer.List(
        "defect",
        message="Which defect would you like to model?",
        choices=["Diamond Nitrogen Vacancy",
                 "SiC Divacancy", "SiC Silicon Vacancy"],
    ),
]
answers = inquirer.prompt(questions)

defect_name = answers["defect"]

if answers["defect"] == "SiC Divacancy":
    questions = [
        inquirer.List(
            "ZPL",
            message="Choose which Silicon vacancy",
            choices=["PL1", "PL2", "PL3", "PL4", "PL5", "PL6", "PL7", "PL8"],
        )
    ]
    answers = inquirer.prompt(questions)
    defect_name = answers["ZPL"]

print(defect_name)
defect = Defect(defect_name)


ax = plt.figure().add_subplot(projection="3d")

B_max = 0.000000000001
B_array = linspace(B_max / 10, B_max, 5)


def evals(B, E, T, theta, phi) -> list:
    M = defect.resolveHamiltonian(T, B, E)
    return list(M.eigenvals().keys())


theta = 0
phi = 0
T_array = linspace(00, 500, 4)
# y_array[2].append(defect.D(300))
E_max = 0.03
for E in linspace(0, E_max, 4):
    opacity = E / E_max * 0.6 + 0.4
    print(opacity)

    for T in T_array:
        y_array = []
        y_array.append([])
        y_array.append([])
        if defect.spin != 1:
            y_array.append([])
            y_array.append([])
        x_array = []

        for B in B_array:
            es = sorted(evals(B, E, T, theta=theta, phi=phi))
            if defect.spin == 1:
                # if len(es) == 2:
                # es.append(es[1])
                x_array.append(B)
                y_array[0].append((es[2] - es[0]))
                y_array[1].append((es[1] - es[0]))
                # y_array[2].append(defect.D(T))

            else:
                es = [num for num in es if abs(num) >= 10**-7]
                if len(es) != 2:
                    x_array.append(B)
                    print(es[0])
                    print(es[1])
                    y_array[0].append(es[0])
                    y_array[1].append(es[1])
                    y_array[2].append(es[2])
                    y_array[3].append(es[3])

        # print(len(es))
        ax.plot(x_array, y_array[0], zs=T, zdir="x",
                c=cm.cool(T / 500), alpha=opacity)
        ax.plot(
            x_array,
            y_array[1],
            zs=T,
            zdir="x",
            c=cm.cool(T / 500),
            alpha=opacity,
        )
        if defect.spin != 1:
            ax.plot(
                x_array,
                y_array[2],
                zs=T,
                zdir="x",
                c=cm.cool(T / 500),
                alpha=opacity,
            )
            ax.plot(
                x_array,
                y_array[3],
                zs=T,
                zdir="x",
                c=cm.cool(T / 500),
                alpha=opacity,
            )

        # ax.plot(x_array, y_array[2], zs=T, zdir="x")
ax.set_xlabel("Temp ($K$)")
ax.set_ylabel("$B_0$")
ax.set_zlabel("")

# D_array = []
# for T in T_array:
#     D_array.append(defect.D(T))
# ax.plot(T_array, D_array, zs=0, zdir="y", label="Temperature Dependence")

plt.show()
