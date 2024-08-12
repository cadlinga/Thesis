from defects.defect_parent import Defect


class SiliconVacancyPL6(Defect):

    def __init__(self):
        super().__init__()

    def name(self):
        return "Silicon Vacancy (PL6)"

    def spin(self):
        return 1

    def D(self, T):
        # D = 1388 * 10**6
        # Diamond Polynomial Fit
        # Need to find the data / coefficients for the SiC fit
        # https://journals.aps.org/prapplied/pdf/10.1103/PhysRevApplied.8.044015

        # 0-300K https://journals.aps.org/prb/pdf/10.1103/PhysRevB.104.125305
        #         D = (1364.6 + 3.5 × 10−3K−1
        # T − 1.8×10−4K−2T 2 − 1.5 × 10−7K−3T 3 + 1.6 × 10−9K−4
        # T 4 − 2.7 × 10−12K−5T 5 )
        d_0 = 1364.6
        d_1 = 3.5 * 10**-3
        d_2 = -1.8 * 10**-4
        d_3 = -1.5 * 10**-7
        d_4 = 1.6 * 10**-9
        d_5 = -2.7 * 10**-12
        D = d_0 + d_1 * T + d_2 * T**2 + d_3 * T**3 + d_4 * T**4 + d_5 * T**5
        D = D + 5  # REMOVE THIS LINE

        return D * 10**6

        return D

    def E(self):
        E = 0.1 * 10**6
        # E = 0
        return E

    def d(self):
        # https://journals.aps.org/prl/pdf/10.1103/PhysRevLett.112.087601
        return {"parallel": 0.35 * self.h, "perp": 25 * self.h}
