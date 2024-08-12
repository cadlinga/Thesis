from numpy import linspace, array
from matplotlib import pyplot

from defects.PL1 import SiliconVacancyPL1
from defects.PL5 import SiliconVacancyPL5
from defects.PL6 import SiliconVacancyPL6
from defects.V2 import SiliconVacancyV2
from ensemble import Ensemble

pl5 = SiliconVacancyPL5()
pl6 = SiliconVacancyPL6()


def makeGraph(T_Array, name):

    PL5_Array = []
    PL6_Array = []
    for T in T_Array:
        PL5_Array.append(pl5.D(T=T))
        PL6_Array.append(pl6.D(T=T))

    PL5_Array = array(PL5_Array) / 10**6
    PL6_Array = array(PL6_Array) / 10**6

    pyplot.plot(T_Array, PL5_Array, label="PL5")
    pyplot.plot(T_Array, PL6_Array, label="PL6")

    pyplot.xlabel("Temperature (K)")
    pyplot.ylabel("$D$ (MHz)")
    pyplot.legend()

    pyplot.title("Temperature Dependence of $D$ for SiC PL5 and PL6 Defect")
    # pyplot.show()
    pyplot.savefig("../figures/" + name)


# T_Array = linspace(0, 550, 100)
# makeGraph(T_Array, "SiC-PL5PL6-D(T)")

T_Array = linspace(250, 350, 100)
makeGraph(T_Array, "SiC-PL5PL6-D(T)-close")
