from matplotlib import pyplot
from numpy import exp, linspace, array, pi
from brokenaxes import brokenaxes
from matplotlib import cm
import matplotlib as mpl

from defects.PL6 import SiliconVacancyPL6
from defects.V2 import SiliconVacancyV2
from ensemble import Ensemble

width = 3 * 10**6
min = 0 * 10**6
max = 1450 * 10**6
peak_depth = 0.1

ensemble = Ensemble()
ensemble.addDefect(SiliconVacancyPL6())
ensemble.addDefect(SiliconVacancyV2())


def addResonantFrequency(frequency, frequency_Array, pl_array):
    F_array_left = linspace(frequency - width, frequency - 1, 10)
    PL_array_left = []
    for f in F_array_left:
        PL_array_left.append(
            1
            + (
                -exp(-((frequency - width) - f) / (width / 6))
                / exp(+width / (width / 6))
            )
            * peak_depth
        )
        # do the same for right

    frequency_Array.extend(F_array_left)
    pl_array.extend(PL_array_left)

    F_array_right = array(F_array_left) + width
    # PL_array_right = array(PL_array_left) * -1
    frequency_Array.extend(F_array_right)
    # pl_array.extend(PL_array_right)
    pl_array.extend(list(reversed(PL_array_left)))


def plotResonantFrequencies(resonantFrequencies, colour, label, offset):

    frequency_Array = [min]
    pl_array = [1]

    resonantFrequencies = sorted(resonantFrequencies)
    for frequency in resonantFrequencies:
        addResonantFrequency(frequency, frequency_Array, pl_array)

    frequency_Array.append(max)
    pl_array.append(1)

    # frequency_Array.append(max)
    # pl_array.append(1)

    # bax.set_ylim(0, 1.3)
    bax.plot(
        array(frequency_Array) / 10**6,
        array(pl_array) + offset - 1,
        alpha=0.5,
        color=colour,
        label=label,
    )
    # bax.legend(loc=4)


fig = pyplot.figure(figsize=(20, 9))
# plotResonantFrequencies(resonantFrequencies)
# pl6 = SiliconVacancyPL6()
# v2 = SiliconVacancyV2()

bax = brokenaxes(
    xlims=((min / 10**6, 300), (1250, max / 10**6)),
    # ylims=((0, 1.3), (0, 1.3)),
    hspace=0.01,
)


# B vs T ################################################
B_max = 3000 * 10**-6
steps = 15

E_max = 5000000

B_array = linspace(0, B_max, steps)
E_array = linspace(0, E_max, 5)

for E in E_array:  # Colour Drive
    for B in B_array:  # Axis Drive
        plotResonantFrequencies(
            ensemble.resonantAngleFrequencies(
                300,
                {"magnitude": B, "theta": 0, "phi": 0},
                {"magnitude": E, "theta": 0, "phi": 0},
            ),
            cm.winter_r(E / E_max),
            "200K, 3.5mT applied",
            B * 10**3,
        )


# Normalizer
norm = mpl.colors.Normalize(vmin=0, vmax=E_max)
# creating ScalarMappable
cmap = pyplot.get_cmap("winter_r")

sm = pyplot.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
pyplot.title("ODMR Spectra for Ensemble " + ensemble.name())
pyplot.xlabel("Frequency", labelpad=30)
pyplot.ylabel("Applied B Field (mT)", labelpad=30)
cax = fig.add_axes([0.92, 0.185, 0.005, 0.666])
pyplot.colorbar(sm, cax=cax, label="$E_\\parallel$ Vm$^{-1}$", pad=0.1)

pyplot.show()
