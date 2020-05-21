from paipan.si_zhu import SiZhu
from paipan.da_yun import DaYun


class PaiPan(SiZhu):
    def __init__(self, date, gender=True, solar=True, da_yun_count=10):
        super().__init__(date, gender, solar)
        self.qi_yun_year = self.qi_yun_shi_jian()
        self.da_yun = DaYun(self.yue_zhu, self.nian_zhu.tian_gan.yin_yang, self.qi_yun_year, self.date.year,
                            self.gender, da_yun_count)

    def ge_ju(self):
        pass

    def xiao_yun(self):
        pass

    def qi_yun_shi_jian(self):
        return 1987


pp = PaiPan('1987/10/13 9:35')
