from sympy import Matrix, pprint
from numpy import sqrt, cos, sin, array
import uuid

mu = 9.2740100657 * 10**-24
h = 6.62607015 * 10**-34
# NATURAL UNITS
mu = mu / h
h = 1


class Defect:
    def __init__(self) -> None:
        self.h = h
        self.mu = mu
        self.name = self.name()
        self.spin = self.spin()
        self.spinMatrices = self.spinMatrices()
        # self.D = self.D(300)
        self.E = self.E()
        self.g = self.g()
        self.d = self.d()
        self.id = uuid.uuid4()
        # self.H = self.resolveHamiltonian()

    def name(self):
        return "Diamond Nitrogen Vacancy"

    def spin(self):
        return 1

    def spinMatrices(self) -> dict:

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
        return {
            "x": 1 / sqrt(2) * Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]]),
            "y": 1j / sqrt(2) * Matrix([[0, -1, 0], [1, 0, -1], [0, 1, 0]]),
            "z": Matrix([[1, 0, 0], [0, 0, 0], [0, 0, -1]]),
            "I": Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
        }

    def D(self, T):
        return 2.8 * 10**9

    def E(self):
        return 0

    def g(self):
        return 2

    def d(self):
        return {"parallel": 0.35 * h, "perp": 17 * h}

    def resolveAngleHamiltonian(self, T, B, E):
        # Zero field D

        if self.spin == 1:
            H_ZF_D = (
                h
                * self.D(T)
                # DO NOT UNCOMMENT FOR S=1
                # * (
                #     self.spinMatrices["z"] ** 2
                #     - (1 / 3 * self.spin * (self.spin + 1)) *
                #     self.spinMatrices["I"]
                # )
                * self.spinMatrices["z"] ** 2
            )

        if self.spin == 1.5:
            H_ZF_D = (
                h
                * self.D(T)
                # * (self.spin * (self.spin + 1))
                * self.spinMatrices["z"] ** 2
            )

        # Zero field E
        H_ZF_E = (
            h * self.E * (self.spinMatrices["x"]
                          ** 2 - self.spinMatrices["y"] ** 2)
        )

        # Zeeman
        B_x = B["magnitude"] * cos(B["phi"]) * sin(B["theta"])
        B_y = B["magnitude"] * sin(B["phi"]) * sin(B["theta"])
        B_z = B["magnitude"] * cos(B["theta"])
        H_Zeeman = (
            self.g
            * mu
            * (
                (self.spinMatrices["x"] * B_x)  # TODO
                + (self.spinMatrices["y"] * B_y)  # TODO
                + (self.spinMatrices["z"] * B_z)
            )
        )

        E_x = E["magnitude"] * cos(E["phi"]) * sin(E["theta"])
        E_y = E["magnitude"] * sin(E["phi"]) * sin(E["theta"])
        E_z = E["magnitude"] * cos(E["theta"])

        H_Stark = (
            self.d["parallel"]
            * E_z
            * self.spinMatrices["z"] ** 2
            * self.spin
            * (self.spin + 1)
        ) - self.d["perp"] * E_x * (
            self.spinMatrices["x"] ** 2 - self.spinMatrices["y"] ** 2
        )
        +self.d["perp"] * E_y * (
            self.spinMatrices["x"] * self.spinMatrices["y"]
            + self.spinMatrices["y"] * self.spinMatrices["x"]
        )

        H = H_ZF_D + H_ZF_E + H_Zeeman + H_Stark
        # H = H_ZF_D + H_ZF_E + H_Zeeman
        # H = H_ZF_D + H_ZF_E
        # H = H_ZF_D

        return H

    def resolveHamiltonian(self, T, B, E):
        # Zero field D
        H_ZF_D = (
            h
            * self.D(T)
            # DO NOT UNCOMMENT FOR S=1
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
        H_Stark = (
            self.d["parallel"]
            * 0
            * self.spinMatrices["z"] ** 2
            * self.spin
            * (self.spin + 1)
        ) - self.d["perp"] * E * (
            self.spinMatrices["x"] ** 2 - self.spinMatrices["y"] ** 2
        )  # TODO replace 0 with E_x
        +self.d["perp"] * 0 * (
            self.spinMatrices["x"] * self.spinMatrices["y"]
            + self.spinMatrices["y"] * self.spinMatrices["x"]
        )  # TODO replace 0 with E_y

        H = H_ZF_D + H_ZF_E + H_Zeeman + H_Stark
        # H = H_ZF_D + H_ZF_E + H_Zeeman
        # H = H_ZF_D + H_ZF_E
        # H = H_ZF_D

        return H

    def angleEvals(self, T, B, E) -> list:
        M = self.resolveAngleHamiltonian(T, B, E)
        return list(M.eigenvals().keys())

    def evals(self, T=0, B=0, E=0) -> list:
        M = self.resolveHamiltonian(T, B, E)
        return list(M.eigenvals().keys())

    def resonantFrequencies(self, T=0, B=0, E=0) -> list:
        evals = self.evals(T, B, E)
        if self.spin == 1:
            if len(evals) == 2:
                return [int(evals[1])]
            else:
                return [int(evals[1]), int(evals[2])]

        if self.spin == 1.5:
            if len(evals) == 2:
                return [int(evals[0] - evals[1])]
            else:
                return [int(abs(evals[2] - evals[0])), int(abs(evals[3] - evals[1]))]

    def resonantAngleFrequencies(self, T, B, E) -> list:
        evals = self.angleEvals(T, B, E)
        if self.spin == 1:
            if len(evals) == 2:
                return [int(evals[1])]
            else:
                return [int(evals[1]), int(evals[2])]

        if self.spin == 1.5:
            if len(evals) == 2:
                return [int(evals[0] - evals[1])]
            else:

                plus = evals[0:3:2]
                minus = evals[1:4:2]
                return [int(max(plus) - min(plus)), int(max(minus) - min(minus))]
                # return [int((evals[2] - evals[0])), int((evals[3] - evals[1]))]

    def __str__(self) -> str:
        print("Name: " + str(self.name) + "\n" +
              "Spin: " + str(self.spin) + "\n")
        print(
            "E: "
            + str(self.E)
            + "\n"
            + "D(300K): "
            + str(self.D(300))
            + "\n"
            + "d: "
            + str(self.d)
            + "\n"
        )

        # print("Spin x = ")
        # pprint(self.spinMatrices["x"])
        #
        # print("Spin y = ")
        # pprint(self.spinMatrices["y"])
        #
        # print("Spin z = ")
        # pprint(self.spinMatrices["z"])

        return "________________________"
