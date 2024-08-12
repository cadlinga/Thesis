from defects.defect_parent import Defect


class DiamondNitrogenVacancy(Defect):

    def __init__(self):
        super().__init__()

    def name(self):
        return "Diamond Nitrogen Vacancy"

    def spin(self):
        return 1

    def D(self, T):
        d_0 = 2.87771
        d_1 = -4.6 * 10**-6
        d_2 = 1.067 * 10**-7
        d_3 = -9.325 * 10**-10
        d_4 = 1.739 * 10**-12
        d_5 = -1.838 * 10**-15
        D = d_0 + d_1 * T + d_2 * T**2 + d_3 * T**3 + d_4 * T**4 + d_5 * T**5
        return D * 10**9

    def d(self):
        return {"parallel": 0.35 * self.h, "perp": 17 * self.h}


defect = DiamondNitrogenVacancy()
