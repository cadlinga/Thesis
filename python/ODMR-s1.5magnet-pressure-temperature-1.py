from matplotlib import pyplot
from mpl_toolkits.axisartist.axislines import SubplotZero
from numpy import exp, linspace, array, pi
from brokenaxes import brokenaxes
from matplotlib import cm
import matplotlib as mpl

from defects.PL6 import SiliconVacancyPL6

from defects.V2 import SiliconVacancyV2
from ensemble import Ensemble

pyplot.rcParams.update({"font.size": 12})

width = 20 * 10**6
min = 170 * 10**6
max = 1600 * 10**6
# min = 1290 * 10**6
# max = 1440 * 10**6
peak_depth = 0.07

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
        alpha=0.9,
        linewidth=1.2,
        color=colour,
        label=label,
    )

    # bax.legend(loc=4)


fig = pyplot.figure(figsize=(9, 4), dpi=300)
ax = SubplotZero(fig, 111)
fig.add_subplot(ax)
#
# for direction in ["yzero"]:
#     #     # adds arrows at the ends of each axis
#     ax.axis[direction].set_axisline_style("-|>")
#     #     # adds X and Y-axis from the origin
#     ax.axis[direction].set_visible(True)
# #
for direction in ["right", "top", "bottom"]:
    # hides borders
    ax.axis[direction].set_visible(False)


# plotResonantFrequencies(resonantFrequencies)
# pl6 = SiliconVacancyPL6()
# v2 = SiliconVacancyV2()

bax = brokenaxes(
    xlims=((min / 10**6, 450), (1150, max / 10**6)),
    # ylims=((5, 6), (5, 6)),
    # hspace=0.01,
)


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
B = 5.4 * 10**-3
plotResonantFrequencies(
    ensemble.resonantAngleFrequencies(
        000,
        {"magnitude": B, "theta": theta, "phi": 0},
        {"magnitude": 0, "theta": 0, "phi": 0},
    ),
    cm.cool(150 / 500),
    # "blue",
    "$B =" + str(B * 10**3) + " $ mT, $P=0$ GPa, T=0 K",
    B * 10**3,
)

bax.axvline(
    x=ensemble.defects[0].D(200) * 10**-6,
    # color="b",
    color=cm.cool(150 / 500),
    alpha=0.5,
    linestyle="dashed",
    linewidth=0.8,
)

d15 = (ensemble.defects[1].D(200) * 10**-6,)
print(d15)

bax.axvline(
    x=ensemble.defects[1].D(200) * 10**-6,
    # color="b",
    color=cm.cool(150 / 500),
    alpha=0.5,
    linestyle="dashed",
    linewidth=0.8,
)

print(
    ensemble.resonantAngleFrequencies(
        0,
        {"magnitude": B, "theta": theta, "phi": 0},
        {"magnitude": 0, "theta": 0, "phi": 0},
    )
)

ensemble.defects[0].setPressure(1)
ensemble.defects[1].setPressure(1)
plotResonantFrequencies(
    ensemble.resonantAngleFrequencies(
        0,
        {"magnitude": B, "theta": theta, "phi": 0},
        {"magnitude": 0, "theta": 0, "phi": 0},
    ),
    cm.cool(350 / 500),
    # "blue",
    "$B =" + str(B * 10**3) + " $ mT, $P=1$ GPa, T=300 K",
    B * 10**3 + 0.003,
)
print(
    ensemble.resonantAngleFrequencies(
        0,
        {"magnitude": B, "theta": theta, "phi": 0},
        {"magnitude": 0, "theta": 0, "phi": 0},
    )
)


bax.axvline(
    x=ensemble.defects[0].D(0) * 10**-6,
    # color="b",
    color=cm.cool(350 / 500),
    alpha=0.5,
    linestyle="dashed",
    linewidth=0.8,
)

# Normalizer
norm = mpl.colors.Normalize(vmin=0, vmax=T_max)
# creating ScalarMappable
cmap = pyplot.get_cmap("jet")

sm = pyplot.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
x = ensemble.defects[0].D(0) / 10**6
# pyplot.axvline(x=x, color="b", alpha=0.5, linestyle="dashed", linewidth=0.8)
pyplot.title("Representative ODMR Spectra for V2, PL6")
pyplot.xlabel("Frequency (MHz)", labelpad=20)
pyplot.ylabel("Photoluminescence Intensity")
# pyplot.yticks([])
ax.set_yticks([])
bax.axs[0].set_yticks([])
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
# bax.legend(loc=8)
bax.legend(bbox_to_anchor=(0.845, 0.4))
# pyplot.savefig("../figures/PL6ODMRSpectra_theta_0_to_90")

# pyplot.tight_layout(pad=0.9)
# pyplot.tight_layout(pad=1.1, rect=(0.00, 0.00, 0.98, 1.01))

pyplot.savefig("../figures/ODMR-multimodal-s15magnet-s1PT")
pyplot.show()
