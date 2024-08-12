from defects.PL6 import SiliconVacancyPL6
from sympy import pprint
from numpy import pi, linspace, array
from matplotlib import pyplot

from defects.V2 import SiliconVacancyV2

# defect = SiliconVacancyPL6()
defect = SiliconVacancyV2()

B_dict = {"magnitude": 5000 * 10**-6, "theta": 0, "phi": 0}
E_dict = {"magnitude": 0, "theta": 0, "phi": 0}
# pprint(defect.resolveAngleHamiltonian(300, B_dict, E_dict))
steps = 50


def makePlot(T, B_dict, E_dict, color, opacity):
    B_array = linspace(10**-12, B_dict["magnitude"], steps)

    F_array = []
    F_array.append([])
    F_array.append([])
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


# plotD(300)
# Baseline
makePlot(300, B_dict, E_dict, "blue", 0.5)
# Warmer
# makePlot(303, B_dict, E_dict, "green", 0.5)

# Applied E field parallel to B field
E_dict = {"magnitude": 5000000, "theta": 0, "phi": 0}
makePlot(300, B_dict, E_dict, "red", 0.5)


# Applied E field perp to B field
# plotD(300)
#
#
# # Baseline
# E_dict = {"magnitude": 0, "theta": 0, "phi": 0}
# makePlot(300, B_dict, E_dict, "blue", 0.5)
#
E_dict = {"magnitude": 5000, "theta": pi / 2, "phi": 0}
makePlot(300, B_dict, E_dict, "purple", 0.5)
#
# # Applied E field perp to B field
#
#
# pyplot.legend()
# pyplot.show()

pyplot.legend()
pyplot.show()
