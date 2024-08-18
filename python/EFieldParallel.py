from defects.PL6 import SiliconVacancyPL6
from mpl_toolkits.axisartist.axislines import SubplotZero
from sympy import pprint
from numpy import pi, linspace, array
from matplotlib import pyplot

from defects.V2 import SiliconVacancyV2

defect = SiliconVacancyPL6()
# defect = SiliconVacancyV2()

B_dict = {"magnitude": 5000 * 10**-6, "theta": 0, "phi": 0}
E_dict = {"magnitude": 0, "theta": 0, "phi": 0}
# pprint(defect.resolveAngleHamiltonian(300, B_dict, E_dict))
steps = 50


pyplot.rcParams.update({"font.size": 12})


def makePlot(T, B_dict, E_dict, color, opacity, label=""):
    B_array = linspace(10**-12, B_dict["magnitude"], steps)

    F_array = []
    F_array.append([])
    F_array.append([])
    if label == "":
        label = (
            "$|\\vec{E}| = "
            + str(E_dict["magnitude"])
            + "$, $\\theta = $"
            + str(E_dict["theta"])
            + ", $\\varphi = "
            + str(E_dict["phi"])
            + "$, $T="
            + str(T)
            + "$"
        )

    print("Plot for " + label)
    for B in B_array:
        evals = defect.angleEvals(
            T, {"magnitude": B, "theta": 0, "phi": 0}, E_dict)

        print(evals)
        if defect.spin == 1:
            F_array[0].append(sorted(evals)[1])
            F_array[1].append(sorted(evals)[2])

        if defect.spin == 1.5:
            F_array[0].append(abs(evals[0] - evals[2]))
            F_array[1].append(abs(evals[1] - evals[3]))

    F_array = array(F_array) / 10**6

    pyplot.plot(B_array, F_array[0], c=color, label=label, alpha=opacity)
    pyplot.plot(B_array, F_array[1], c=color, alpha=opacity)


def plotD(T):
    B_array = linspace(0, B_dict["magnitude"], steps)
    D_array = []
    for B in B_array:
        D_array.append(defect.D(T))
    D_array = array(D_array) / 10**6

    label = "D @ " + str(T) + "K"
    pyplot.plot(B_array, D_array, c="k", label="D @ 300K")


print(
    defect.angleEvals(
        300,
        {"magnitude": 10**-8, "theta": 0, "phi": 0},
        {"magnitude": 0, "theta": 0, "phi": 0},
    )
)

fig = pyplot.figure(figsize=(8, 4), dpi=300)
ax = SubplotZero(fig, 111)
fig.add_subplot(ax)
#
# for direction in ["yzero"]:
#     # adds arrows at the ends of each axis
#     ax.axis[direction].set_axisline_style("-|>")
#     # adds X and Y-axis from the origin
#     ax.axis[direction].set_visible(True)
#
for direction in ["right", "top"]:
    # hides borders
    ax.axis[direction].set_visible(False)

# plotD(300)
# Baseline

makePlot(300, B_dict, E_dict, "black", 0.8, label="$E = 0$")
# Warmer
# makePlot(303, B_dict, E_dict, "green", 0.5)

# Applied E field parallel to B field
# E_dict = {"magnitude": 5000000, "theta": 0, "phi": 0}
# makePlot(300, B_dict, E_dict, "red", 0.8)


# Applied E field perp to B field
# plotD(300)
#
#
# # Baseline
# E_dict = {"magnitude": 0, "theta": 0, "phi": 0}
# makePlot(300, B_dict, E_dict, "blue", 0.5)
#
E_dict = {"magnitude": 50000000, "theta": 0, "phi": 0}
makePlot(300, B_dict, E_dict, "blue", 0.8, "E > 0")
#
# # Applied E field perp to B field
#

# pyplot.arrow(0, 1100, 0.000006, 0)
pyplot.xlabel("$B$ (mT)")
pyplot.ylabel("EPR Frequency")
pyplot.title(
    "$S=1$ Energy Eigenvalues With Applied $\\vec{E}$, $\\theta = 0^\circ$")
pyplot.legend(loc=7)
# pyplot.show()
pyplot.savefig("../figures/EFieldParallel")
