from matplotlib import pyplot
from mpl_toolkits.axisartist.axislines import SubplotZero
from numpy import exp, linspace, array, pi
from brokenaxes import brokenaxes
from matplotlib import cm
import matplotlib as mpl

from defects.PL6 import SiliconVacancyPL6

# from defects.V2 import SiliconVacancyV2
from ensemble import Ensemble

pyplot.rcParams.update({"font.size": 12})

width = 20 * 10**6
# min = 1290 * 10**6
# max = 1440 * 10**6
min = 900 * 10**6
max = 1800 * 10**6
peak_depth = 0.07

ensemble = Ensemble()
ensemble.addDefect(SiliconVacancyPL6())
# ensemble.addDefect(SiliconVacancyV2())


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
    pyplot.plot(
        array(frequency_Array) / 10**6,
        array(pl_array) + offset - 1,
        alpha=0.7,
        linewidth=0.9,
        color=colour,
        label=label,
    )
    # bax.legend(loc=4)


fig = pyplot.figure(figsize=(6, 4), dpi=300)
ax = SubplotZero(fig, 111)
fig.add_subplot(ax)
#
# for direction in ["yzero"]:
#     #     # adds arrows at the ends of each axis
#     ax.axis[direction].set_axisline_style("-|>")
#     #     # adds X and Y-axis from the origin
#     ax.axis[direction].set_visible(True)
# #
for direction in ["right", "top"]:
    # hides borders
    ax.axis[direction].set_visible(False)


# plotResonantFrequencies(resonantFrequencies)
# pl6 = SiliconVacancyPL6()
# v2 = SiliconVacancyV2()

# bax = brokenaxes(
#     xlims=((min / 10**6, 140), (1320, max / 10**6)),
#     # ylims=((0, 1.3), (0, 1.3)),
#     hspace=0.01,
# )


# B vs T ################################################
B_max = 2000 * 10**-6
steps = 1

T_max = pi / 2

B_array = linspace(0, B_max, steps)
T_array = linspace(0, T_max, 1)

# for t in T_array:  # Colour Drive
#     for B in B_array:  # Axis Drive
#         plotResonantFrequencies(
#             ensemble.resonantAngleFrequencies(
#                 300,
#                 {"magnitude": B, "theta": t, "phi": 0},
#                 {"magnitude": 0, "theta": 0, "phi": 0},
#             ),
#             cm.jet(t / T_max),
#             "200K, 3.5mT applied",
#             B * 10**3,
#         )
#

theta = pi / 6
theta = 0
B = 13.4 / 2 * 10**-3
plotResonantFrequencies(
    ensemble.resonantAngleFrequencies(
        0,
        {"magnitude": B, "theta": theta, "phi": 0},
        {"magnitude": 0, "theta": 0, "phi": 0},
    ),
    # cm.jet(theta / T_max),
    "blue",
    "$B =" + str(B * 10**3) + " $ mT, $\\theta = 0^\\circ$",
    B * 10**3,
)
# Normalizer
norm = mpl.colors.Normalize(vmin=0, vmax=T_max)
# creating ScalarMappable
cmap = pyplot.get_cmap("jet")

sm = pyplot.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
pyplot.title("Representative ODMR Spectra for PL6 ($S=1$)")
pyplot.xlabel("Frequency (MHz)")
pyplot.ylabel("Photoluminescence Intensity")
pyplot.yticks([])
pyplot.ylim([(13.41 / 2) - 0.21, 13.41 / 2])
x = ensemble.defects[0].D(0) / 10**6
pyplot.axvline(x=x, color="b", alpha=0.5, linestyle="dashed", linewidth=0.8)
# offset = ensemble.defects[0].D(300) / 10**6
# pyplot.ticklabel_format(axis="x", useOffset=offset)
# cax = fig.add_axes([0.92, 0.185, 0.005, 0.666])
# cbar = pyplot.colorbar(
#     sm,
#     cax=cax,
#     label="Angle (radians)",
#     # pad=-0.5,
#     ticks=[0, pi / 4, pi / 2],
# )
# cbar.ax.yaxis.set_ticks_position("left")
# cbar.ax.yaxis.set_label_position("left")
#
# cbar.ax.set_yticklabels(["$0$", "$\\pi / 4$", "$\\pi /2$"])

# pyplot.tight_layout(pad=1.1, rect=(0.03, 0, 0.80, 1))
# pyplot.tight_layout()
pyplot.legend(loc=7, handlelength=0, handletextpad=0)
pyplot.savefig("../figures/ODMR-s1magnet-3")

pyplot.show()
