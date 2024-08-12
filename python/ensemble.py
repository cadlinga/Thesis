from defects.defect_parent import Defect
from defects.dnv import DiamondNitrogenVacancy
from defects.PL1 import SiliconVacancyPL1
from defects.PL6 import SiliconVacancyPL6
from defects.PL5 import SiliconVacancyPL5
from defects.V2 import SiliconVacancyV2
from numpy import linspace, who, array
from scipy.interpolate import interp1d
import matplotlib as mpl
import numpy as np
import matplotlib.lines as mlines


import matplotlib.pyplot as plt
from matplotlib import cm


class Ensemble:
    def __init__(self):
        self.defects = []
        self.T = (250, 350)
        self.B = (0.01 * 10**-6, 100 * 10**-6)
        self.E = (0, 5 / 100)

    def addDefect(self, defect):
        self.defects.append(defect)

    def __str__(self):
        for defect in self.defects:
            print(defect)

        return "________________"

    def name(self):
        name = "("
        # name = ""
        for defect in self.defects:
            name += defect.name

        name += ")"

        return name

    def resonantFrequencies(self, T, B, E):
        if len(self.defects) == 0:
            return []

        freqs = []
        for defect in self.defects:
            freqs.extend(defect.resonantFrequencies(T, B, E))

        return freqs

    def resonantAngleFrequencies(self, T, B, E):
        if len(self.defects) == 0:
            return []

        freqs = []
        for defect in self.defects:
            freqs.extend(defect.resonantAngleFrequencies(T, B, E))

        return freqs

    def make3Dplot(self, defect):
        T_array = linspace(self.T[0], self.T[1], 3)
        B_array = linspace(self.B[0], self.B[1], 25)
        E_array = linspace(self.E[0], self.E[1], 1)

        E_array = [self.E[1]]

        # if defect.spin == 1.5:
        # E_array = [self.E[1]]
        # T_array = [self.T[1]]

        # for B in B_array:
        # print(sorted(defect.evals(0, B, 300)))
        # return
        ax = plt.figure().add_subplot(projection="3d")

        for E in E_array:
            opacity = (E / self.E[1]) * 0.6 + 0.1

            for T in T_array:
                y_array = []
                y_array.append([])
                y_array.append([])
                if defect.spin != 1:
                    y_array.append([])
                    y_array.append([])
                x_array = []

                for B in B_array:
                    es = defect.evals(T, B, E)
                    if defect.spin == 1:
                        es = sorted(es)
                        x_array.append(B)
                        if 0 in es and len(es) == 2:
                            y_array[0].append((es[1] - es[0]))
                            y_array[1].append((es[1] - es[0]))
                        else:
                            y_array[0].append((es[2] - es[0]))
                            y_array[1].append((es[1] - es[0]))

                    else:
                        # es = [num for num in es if abs(num) >= 10**-7]

                        x_array.append(B)
                        if len(es) != 2:
                            y_array[0].append(abs(es[3] - es[1]))
                            y_array[1].append(abs(es[2] - es[0]))
                            # y_array[2].append(es[2])
                            # y_array[3].append(es[3])
                        else:
                            y_array[0].append(es[0])
                            y_array[1].append(es[0])
                            # y_array[2].append(es[1])
                            # y_array[3].append(es[1])

                y_array = array(y_array) / 10**6
                ax.plot(
                    x_array,
                    y_array[0],
                    zs=T,
                    zdir="x",
                    # c=cm.cool(T / self.T[1]),
                    c=cm.cool((T - self.T[0]) / (self.T[1] - self.T[0])),
                    alpha=opacity,
                )
                ax.plot(
                    x_array,
                    y_array[1],
                    zs=T,
                    zdir="x",
                    # c=cm.cool(T / self.T[1]),
                    c=cm.cool((T - self.T[0]) / (self.T[1] - self.T[0])),
                    alpha=opacity,
                )
        ax.set_xlabel("Temp ($K$)")
        ax.set_ylabel("$B_0$ (T)")
        ax.set_zlabel("EPR Frequency (MHz)")

        if defect.spin == 1:
            D_array = []
            for T in T_array:
                D_array.append(defect.D(T))

            D_array = array(D_array) / 10**6
            ax.plot(T_array, D_array, zs=0, zdir="y",
                    label="$D$ as a function of $T$")
            # ax.plot(T_array, D_array,
            # zs=self.B[1], zdir="y", label="$(f_1 + f_2)/2$")

        plt.title(
            "$D$ and EPR Frequency with known $B_0$ for SiC PL6 vs. Temperature")
        plt.legend()
        plt.show()

    def makePLplot(self, parameters):
        # T_array = linspace(self.T[0], self.T[1], 3)
        # B_array = linspace(self.B[0], self.B[1], 3)
        # E_array = linspace(self.E[0], self.E[1], 3)

        resonant_frequencies = []

        for defect, T, B, E in parameters:
            resonant_frequencies.append(defect.evals(T, B, E))

        print(resonant_frequencies)
        x_lims = [0, 4 * 10**9]
        x_lims = []

        for f_array in resonant_frequencies:
            f_array = [num for num in f_array if abs(num) != 0]

            if len(f_array) == 1:
                x_lims.append(f_array[0] * 1.0001)
                x_lims.append(f_array[0] * 0.9999)
            else:
                difference = max(f_array) - min(f_array)
                x_lims.append(min(f_array) - 1 * difference)
                x_lims.append(max(f_array) + 1 * difference)

        x_array = linspace(float(min(x_lims)), float(max(x_lims)), 1000)

        # for f_array in resonant_frequencies:
        for defect, T, B, E in parameters:
            evals = defect.evals(T, B, E)
            f_array = [num for num in evals if abs(num) != 0]

            y_array = []
            f_array = [num for num in f_array if abs(num) != 0]
            for x in x_array:
                y = 1
                diff = []
                for f in f_array:
                    diff.append(abs(x - f))
                diff = min(diff)
                width = 50000
                if diff <= width:
                    y = 1 - 0.4 * (diff / width)
                    y = 0.6  # y = -1 / ((diff) ** 0.00000001)
                y_array.append(y)
                title = "CW-ODMR Plot for ensemble"
                label = (
                    defect.name
                    + ", $B = "
                    + str(B)
                    + "$, $E = "
                    + str(E)
                    + "$, $T="
                    + str(T)
                    + "$ \n"
                    + str(f_array)
                )
            plt.title(title)
            plt.plot(x_array, y_array, label=label, alpha=0.6)
        plt.ylim(0, 1.1)
        # plt.xlim(
        #     0,
        # )
        # plt.xlim(28 * 10**8, 29 * 10**8)
        plt.legend()
        plt.show()

    def makePairwiseEplot(self, defects):
        # fig, defects[0].id = plt.subplots(1, 1, figsize=(8, 6))
        fig, ax1 = plt.subplots(1, 1, figsize=(16, 16))
        T = 0
        # B = self.B[0]
        # T_array = linspace(self.T[0], self.T[1], 3)
        B_array = linspace(self.B[0], self.B[1], 10)
        E_array = linspace(self.E[0], self.E[1], 3)

        # for i in range(len(defects)):
        #     if i != 0:
        #         (defects[i].id).(defects[0].id).twinx
        ax2 = ax1.twinx()

        # for defect in defects:
        #     D = defect.D(T)
        #
        #     for E in E_array:
        #         f_array = []
        #         for B in B_array:
        #             evals = defect.evals(T, B, E)
        #             f_array.append(max(evals))
        #             print(max(evals))
        #
        #         defects[0].id.plot(B_array * 10**6, f_array,
        #                            c=cm.cool(E / self.E[1]))
        #
        #     defects[0].id.set_ylabel(defect.name + " EPR Resonance Frequency")
        for E in E_array:
            f_array = []
            print("E = " + str(E))
            for B in B_array:
                evals = defects[0].evals(T, B, E)
                if defects[0].spin == 1:
                    f_array.append(max(evals))
                else:
                    es = evals
                    print(es)
                    if len(es) != 2:
                        # f_array.append(abs(es[3] - es[1]))
                        f_array.append(abs(es[2] - es[0]))
                    else:
                        f_array.append(es[0])
                        # f_array.append(es[1])

            ax1.plot(
                B_array * 10**6,
                np.array(f_array) * 10**-6,
                # f_array,
                c=cm.cool(E / self.E[1]),
                # alpha=0.5,
                marker="o",
                mfc="blue",
                mec="k",
                markersize="8",
            )

        ax1.set_ylabel(defects[0].name + " EPR Resonance Frequency (MHz)")
        ax2.set_ylabel(defects[1].name + " EPR Resonance Frequency (MHz)")
        # ax2.set_ylim(460000 + 1.364 * 10**9, 780000 + 1.364 * 10**9)
        # ax1.set_ylim(700000 + 2.877 * 10**9, 1050000 + 2.877 * 10**9)

        for E in E_array:
            f_array = []
            for B in B_array:
                evals = defects[1].evals(T, B, E)
                if defects[1].spin == 1:
                    f_array.append(max(evals))
                else:
                    es = evals
                    print(es)
                    if len(es) != 2:
                        # f_array.append(abs(es[3] - es[1]))
                        f_array.append(abs(es[2] - es[0]))
                    else:
                        f_array.append(es[0])
                        # f_array.append(es[1])

            ax2.plot(
                B_array * 10**6,
                np.array(f_array) * 10**-6,
                c=cm.cool(E / self.E[1]),
                # alpha=0.5,
                marker="*",
                mfc="red",
                mec="k",
                markersize="8",
            )
            ax1.ticklabel_format(useOffset=False)
            ax2.ticklabel_format(useOffset=False)

        # Normalizer
        norm = mpl.colors.Normalize(vmin=self.E[0] / 100, vmax=self.E[1] / 100)

        # creating ScalarMappable
        cmap = plt.get_cmap("cool")
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])

        plt.colorbar(
            sm, ax=ax1, label="Applied $E$ field V cm$^{-1}$", pad=0.1)
        ax1.set_xlabel("Applied $B$ field ($\mu$T)")

        star = mlines.Line2D(
            [],
            [],
            marker="*",
            linestyle="None",
            markersize=10,
            label=defects[1].name,
            mfc="red",
            mec="k",
        )
        circle = mlines.Line2D(
            [],
            [],
            marker="o",
            linestyle="None",
            markersize=10,
            label=defects[0].name,
            mfc="blue",
            mec="k",
        )

        plt.legend(handles=[star, circle])
        plt.show()

    def makePairwiseTplot(self, defects):
        # fig, defects[0].id = plt.subplots(1, 1, figsize=(8, 6))
        fig, ax1 = plt.subplots(1, 1, figsize=(16, 16))
        E = 0
        # B = self.B[0]
        # T_array = linspace(self.T[0], self.T[1], 3)
        B_array = linspace(self.B[0], self.B[1], 10)
        T_array = linspace(self.T[0], self.T[1], 3)

        # for i in range(len(defects)):
        #     if i != 0:
        #         (defects[i].id).(defects[0].id).twinx
        ax2 = ax1.twinx()

        # for defect in defects:
        #     D = defect.D(T)
        #
        #     for E in E_array:
        #         f_array = []
        #         for B in B_array:
        #             evals = defect.evals(T, B, E)
        #             f_array.append(max(evals))
        #             print(max(evals))
        #
        #         defects[0].id.plot(B_array * 10**6, f_array,
        #                            c=cm.cool(E / self.E[1]))
        #
        #     defects[0].id.set_ylabel(defect.name + " EPR Resonance Frequency")
        for T in T_array:
            f_array = []
            for B in B_array:
                evals = defects[0].evals(T, B, E)
                if defects[0].spin == 1:
                    f_array.append(max(evals))
                else:
                    es = evals
                    if len(es) != 2:
                        # f_array.append(abs(es[3] - es[1]))
                        f_array.append(abs(es[2] - es[0]))
                    else:
                        f_array.append(es[0])
                        # f_array.append(es[1])

            ax1.plot(
                B_array * 10**6,
                # f_array,
                np.array(f_array) * 10**-6,
                c=cm.cool((T - self.T[0]) / (self.T[1] - self.T[0])),
                # alpha=0.5,
                marker="o",
                mfc="blue",
                mec="k",
                markersize="8",
            )
            f_array = []
            for B in B_array:
                evals = defects[0].evals(T, B, E)
                if defects[0].spin == 1:
                    f_array.append(max(evals))
                else:
                    es = evals
                    if len(es) != 2:
                        f_array.append(abs(es[3] - es[1]))
                        # f_array.append(abs(es[2] - es[0]))
                    else:
                        f_array.append(es[0])
                        # f_array.append(es[1])

            ax1.plot(
                B_array * 10**6,
                # f_array,
                np.array(f_array) * 10**-6,
                c=cm.cool((T - self.T[0]) / (self.T[1] - self.T[0])),
                # alpha=0.5,
                marker="o",
                mfc="blue",
                mec="k",
                markersize="8",
            )

        ax1.set_ylabel(defects[0].name + " EPR Resonance Frequency (MHz)")
        ax2.set_ylabel(defects[1].name + " EPR Resonance Frequency (MHz)")

        for T in T_array:
            f_array = []
            for B in B_array:
                evals = defects[1].evals(T, B, E)
                if defects[1].spin == 1:
                    f_array.append(max(evals))
                else:
                    es = evals
                    print(es)
                    if len(es) != 2:
                        # f_array.append(abs(es[3] - es[1]))
                        f_array.append(abs(es[2] - es[0]))
                    else:
                        f_array.append(es[0])
                        # f_array.append(es[1])

            ax2.plot(
                B_array * 10**6,
                # f_array,
                np.array(f_array) * 10**-6,
                c=cm.cool((T - self.T[0]) / (self.T[1] - self.T[0])),
                # alpha=0.5,
                marker="*",
                mfc="red",
                mec="k",
                markersize="8",
            )
            f_array = []
            for B in B_array:
                evals = defects[1].evals(T, B, E)
                if defects[1].spin == 1:
                    f_array.append(sorted(evals)[1])
                else:
                    es = evals
                    print(es)
                    if len(es) != 2:
                        # f_array.append(abs(es[3] - es[1]))
                        f_array.append(abs(es[2] - es[0]))
                    else:
                        f_array.append(es[0])
                        # f_array.append(es[1])

            ax2.plot(
                B_array * 10**6,
                # f_array,
                np.array(f_array) * 10**-6,
                c=cm.cool((T - self.T[0]) / (self.T[1] - self.T[0])),
                # alpha=0.5,
                marker="*",
                mfc="red",
                mec="k",
                markersize="8",
            )

        ax1.set_ylabel(defects[0].name + " EPR Resonance Frequency")

        ax1.ticklabel_format(useOffset=False)
        ax2.ticklabel_format(useOffset=False)

        # Normalizer
        norm = mpl.colors.Normalize(vmin=self.T[0], vmax=self.T[1])

        # creating ScalarMappable
        cmap = plt.get_cmap("cool")
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])

        plt.colorbar(sm, ax=ax1, label="Temperature (K)", pad=0.1)
        ax1.set_xlabel("Applied $B$ field ($\mu$T)")

        star = mlines.Line2D(
            [],
            [],
            marker="*",
            linestyle="None",
            markersize=10,
            label=defects[1].name,
            mfc="red",
            mec="k",
        )
        circle = mlines.Line2D(
            [],
            [],
            marker="o",
            linestyle="None",
            markersize=10,
            label=defects[0].name,
            mfc="blue",
            mec="k",
        )

        plt.legend(handles=[star, circle])
        plt.show()

    def makePLplot2(self, parameters):
        resonant_frequencies = []

        for defect, T, B, E in parameters:
            evals = defect.evals(T, B, E)
            if defect.spin == 1.5:
                if len(evals) != 2:
                    resonant_frequencies.append(evals[3] - evals[0])
                    resonant_frequencies.append(evals[2] - evals[1])

        x_lims = [0, 4 * 10**7]
        # x_lims = [0.9 * min(resonant_frequencies), 1.1 *
        # max(resonant_frequencies)]

        x_array = linspace(float(min(x_lims)), float(max(x_lims)), 1000)

        # for f_array in resonant_frequencies:
        for defect, T, B, E in parameters:
            evals = defect.evals(T, B, E)
            f_array = [num for num in evals if abs(num) != 0]

            y_array = []
            f_array = [num for num in f_array if abs(num) != 0]
            for x in x_array:
                y = 1
                diff = []
                for f in f_array:
                    diff.append(abs(x - f))
                diff = min(diff)
                width = 10000
                if diff <= width:
                    y = 1 - 0.4 * (diff / width)
                    y = 0.6  # y = -1 / ((diff) ** 0.00000001)
                y_array.append(y)
                title = "CW-ODMR Plot for ensemble"
                label = (
                    defect.name
                    + ", $B = "
                    + str(B)
                    + "$, $E = "
                    + str(E)
                    + "$, $T="
                    + str(T)
                    + "$ \n"
                    + str(f_array)
                )
            plt.title(title)
            plt.plot(x_array, y_array, label=label, alpha=0.6)
        plt.ylim(0, 1.1)
        # plt.xlim(28 * 10**8, 29 * 10**8)
        plt.legend()
        plt.show()


# ensemble = Ensemble()
# ensemble.addDefect(DiamondNitrogenVacancy())
# ensemble.addDefect(SiliconVacancyPL1())

# ensemble.make3Dplot(ensemble.defects[0])
# ensemble.makePLplot(
#     [
#         # (ensemble.defects[0], 300, 0.001, 5),
#         # (ensemble.defects[0], 320, 0.001, 5),
#         (ensemble.defects[0], 300, 0, 0),
#         (ensemble.defects[0], 300, 10**-4, 0),
#         (ensemble.defects[0], 350, 10**-4, 0),
#         # (ensemble.defects[1], 300, 0.001, 5 * 10**5),
#         # (ensemble.defects[0], 300, 0.005, 5),
#         # (ensemble.defects[1], 300, 0.005, 5 * 10**5),
#         # (ensemble.defects[0], 300, 10**-7, 5),
#     ]
# )

# ensemble.makePairwiseEplot((ensemble.defects[0], ensemble.defects[1]))
# ensemble.makePairwiseTplot((ensemble.defects[0], ensemble.defects[1]))


# ensemble = Ensemble()
# ensemble.addDefect(SiliconVacancyV2())
# ensemble.addDefect(SiliconVacancyPL5())
# ensemble.addDefect(SiliconVacancyPL6())
# ensemble.addDefect(DiamondNitrogenVacancy())


# ensemble.make3Dplot(ensemble.defects[0])

# ensemble.makePairwiseTplot((ensemble.defects[0], ensemble.defects[1]))
# ensemble.makePairwiseTplot((ensemble.defects[0], ensemble.defects[1]))

# print(ensemble.defects[0].evals(300, 0, 0))
# print(ensemble.defects[0].evals(300, 10**-7, 0))
# print(ensemble.defects[0].evals(300, 5 * 10**-7, 0))

# ensemble.makePLplot(
#     [
#         # (ensemble.defects[0], 300, 0.001, 5),
#         # (ensemble.defects[0], 320, 0.001, 5),
#         # (ensemble.defects[0], 300, 2 * 10**-4, 0),
#         (ensemble.defects[0], 300, 10**-6, 0),
#         (ensemble.defects[0], 300, 10**-4, 0),
#         (ensemble.defects[0], 300, 10**-3, 0),
#         # (ensemble.defects[1], 300, 10**-3, 0),
#         # (ensemble.defects[1], 300, 0.001, 5 * 10**5),
#         # (ensemble.defects[0], 300, 0.005, 5),
#         # (ensemble.defects[1], 300, 0.005, 5 * 10**5),
#         # (ensemble.defects[0], 300, 10**-7, 5),
#     ]
# )
#
#
# print(ensemble.defects[0].evals(T=0, B=1 * 10**-10, E=0))
# print(ensemble)
