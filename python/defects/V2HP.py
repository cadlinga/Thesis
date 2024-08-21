from defects.defect_parent import Defect


class SiliconVacancyV2(Defect):

    def __init__(self):
        super().__init__()

    def name(self):
        return "Silicon Vacancy (V2)"

    def spin(self):
        return 1.5

    def D(self, T):
        D = 40 * 10**6
        return D

    def E(self):
        E = 0
        return E

    def d(self):
        # https://journals.aps.org/prl/pdf/10.1103/PhysRevLett.112.087601
        return {"parallel": 0.35 * self.h, "perp": 25 * self.h}
