from matplotlib import pyplot
from mpl_toolkits.axisartist.axislines import SubplotZero
from numpy import exp, linspace, array
from brokenaxes import brokenaxes
from matplotlib import cm
import matplotlib as mpl

from defects.PL6 import SiliconVacancyPL6
from defects.V2 import SiliconVacancyV2
from ensemble import Ensemble

width = 1.5 * 10**6
min = 1345 * 10**6
max = 1380 * 10**6
peak_depth = 0.02

ensemble = Ensemble()
ensemble.addDefect(SiliconVacancyPL6())
# ensemble.addDefect(SiliconVacancyV2())

pyplot.rcParams.update({"font.size": 12})


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
    # bax.plot(
    pyplot.plot(
        array(frequency_Array) / 10**6,
        array(pl_array) + offset - 1,
        alpha=0.5,
        color=colour,
        label=label,
    )
    # bax.legend(loc=4)


# fig = pyplot.figure(figsize=(20, 9))
# fig = pyplot.figure(figsize=(8, 4), dpi=300)
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


# plotResonantFrequencies(resonantFrequencies)
# pl6 = SiliconVacancyPL6()
# v2 = SiliconVacancyV2()

# bax = brokenaxes(
#     xlims=((min / 10**6, 300), (1100, max / 10**6)),
#     # ylims=((0, 1.3), (0, 1.3)),
#     hspace=0.01,
# )


# B vs T ################################################
B_max = 300 * 10**-6
steps = 10

T_max = 300

B_array = linspace(0, B_max, steps)
T_array = linspace(0, T_max, 3)
theta_array = linspace(0, 360, steps)

for T in T_array:  # Colour Drive
    for B in B_array:  # Axis Drive
        plotResonantFrequencies(
            ensemble.resonantAngleFrequencies(
                T,
                {"magnitude": B, "theta": 0, "phi": 0},
                {"magnitude": 0, "theta": 0, "phi": 0},
            ),
            cm.cool(T / 300),
            "200K, 3.5mT applied",
            B * 10**3,
        )


# Normalizer
norm = mpl.colors.Normalize(vmin=0, vmax=T_max)
# creating ScalarMappable
cmap = pyplot.get_cmap("cool")

sm = pyplot.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
# pyplot.title("ODMR Spectra for Ensemble " + ensemble.name())

pyplot.title("Representative ODMR Spectra for PL6 ($S=1$)")
pyplot.xlabel("Frequency")
pyplot.ylabel("Applied B Field")
pyplot.yticks([])
cax = fig.add_axes([0.82, 0.185, 0.005, 0.666])
pyplot.colorbar(sm, cax=cax, label="Temperature (T)", pad=0)
pyplot.tight_layout(pad=1.1, rect=(0.03, 0.01, 0.80, 1.01))
# pyplot.show()
pyplot.savefig("../figures/ODMR-s1-temp-dependence")
