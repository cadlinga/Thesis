from sympy import Matrix, pprint
from numpy import sqrt

mu = 9.2740100657 * 10**-24
h = 6.62607015 * 10**-34

# NATURAL UNITS
mu = mu / h
h = 1


class Defect(object):

    def __init__(self, name) -> None:
        self.name = name
        self.spin = self.resolveSpin()
        self.spinMatrices = self.resolveSpinMatrices()
        # self.D = self.resolveD()
        self.E = self.resolveE()
        self.g = self.resolveg()
        self.d = self.resolved()
        # self.H = self.resolveHamiltonian()

    def resolveSpin(self):
        # ["Diamond Nitrogen Vacancy",
        # "SiC Divacancy", "SiC Silicon Vacancy"]
        if self.name == "SiC Silicon Vacancy":
            return 1.5
        else:
            return 1

    def resolveSpinMatrices(self):
        if self.spin == 1:
            return {
                "x": 1 / sqrt(2) * Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]]),
                "y": 1j / sqrt(2) * Matrix([[0, -1, 0], [1, 0, -1], [0, 1, 0]]),
                "z": Matrix([[1, 0, 0], [0, 0, 0], [0, 0, -1]]),
                "I": Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
            }
        if self.spin == 1.5:
            return {
                "x": 1
                / 2
                * Matrix(
                    [
                        [0, sqrt(3), 0, 0],
                        [sqrt(3), 0, 2, 0],
                        [0, 2, 0, sqrt(3)],
                        [0, 0, sqrt(3), 0],
                    ]
                ),
                "y": 1
                / 2j
                * Matrix(
                    [
                        [0, sqrt(3), 0, 0],
                        [-sqrt(3), 0, 2, 0],
                        [0, -2, 0, sqrt(3)],
                        [0, 0, -sqrt(3), 0],
                    ]
                ),
                "z": Matrix(
                    [
                        [3 / 2, 0, 0, 0],
                        [0, 1 / 2, 0, 0],
                        [0, 0, -1 / 2, 0],
                        [0, 0, 0, -3 / 2],
                    ]
                ),
                "I": Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]),
            }

    # def resolveD(self):
    #     return 2.87 * 10**9

    def resolveE(self):
        # return 0.002
        return 0

    def resolveg(self):
        return 2

    def resolved(self):
        return {"parallel": 0.35 * h, "perp": 17 * h}

    def resolveHamiltonian(self, T, B, E):
        # Zero field D
        H_ZF_D = (
            h
            * self.D(T)
            # * (
            #     self.spinMatrices["z"] ** 2
            #     - (1 / 3 * self.spin * (self.spin + 1)) *
            #     self.spinMatrices["I"]
            # )
            * self.spinMatrices["z"] ** 2
        )

        # Zero field E
        H_ZF_E = (
            h * self.E * (self.spinMatrices["x"]
                          ** 2 - self.spinMatrices["y"] ** 2)
        )

        # Zeeman
        H_Zeeman = (
            self.g
            * mu
            * (
                (self.spinMatrices["x"] * 0)  # TODO
                + (self.spinMatrices["y"] * 0)  # TODO
                + (self.spinMatrices["z"] * B)
            )
        )

        # TODO write E field in components
        H_Stark = self.d["parallel"] * E * self.spinMatrices["z"] ** 2
        -self.d["perp"] * 0 * (
            self.spinMatrices["x"] ** 2 - self.spinMatrices["y"] ** 2
        )  # TODO replace 0 with E_x
        +self.d["perp"] * 0 * (
            self.spinMatrices["x"] * self.spinMatrices["y"]
            + self.spinMatrices["y"] * self.spinMatrices["x"]
        )  # TODO replace 0 with E_y

        H = H_ZF_D + H_ZF_E + H_Zeeman + H_Stark
        # H = H_ZF_D + H_Zeeman

        return H

    def __str__(self) -> str:
        print("Name: " + str(self.name) + "\n" + "Spin: " + str(self.spin))

        print("Spin x = ")
        pprint(self.spinMatrices["x"])

        print("Spin y = ")
        pprint(self.spinMatrices["y"])

        print("Spin z = ")
        pprint(self.spinMatrices["z"])

        return "________________________"

    def D(self, T=0):
        if self.name == "Diamond Nitrogen Vacancy":
            d_0 = 2.87771 * 10**9
            d_1 = -4.6 * 10**-6
            d_2 = 1.067 * 10**-7
            d_3 = -9.325 * 10**-10
            d_4 = 1.739 * 10**-12
            d_5 = -1.838 * 10**-15
            D = d_0 + d_1 * T + d_2 * T**2 + d_3 * T**3 + d_4 * T**4 + d_5 * T**5
            return D
        if self.name == "SiC Silicon Vacancy":
            D = 35 * 10**6
            return D

    def Sz_squared(self):
        pprint(self.spinMatrices["z"] ** 2)
        pass

    pass
