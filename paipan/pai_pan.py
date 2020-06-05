from common import *
from paipan.si_zhu import SiZhu
from paipan.da_yun import DaYun
from paipan.qi_yun_shi_jian import QiYunShiJian
from common.calendar import Calendar
from paipan.xiao_yun import XiaoYun


class PaiPan(SiZhu):
    calendar = Calendar()

    def __init__(self, date, gender=True, solar=True, da_yun_count=10, ge_ju_algorithm=None):
        super().__init__(date, gender, solar)
        self.qi_yun_time = self.qi_yun_shi_jian()
        self.da_yun = DaYun(self.yue_zhu,
                            self.nian_zhu.tian_gan.yin_yang,
                            self.qi_yun_time.year,
                            self.date.year,
                            self.gender,
                            da_yun_count)
        self.tai_yuan = self.get_tai_yuan()
        self.xiao_yun_list, self.xiaoyun_ob = self.get_xiao_yun()
        self.ge_ju_algorithm = ge_ju_algorithm

    def ge_ju(self):
        pass

    def get_tai_yuan(self):
        """
        获取胎元
        :return:JiaZi
        """
        taiyuan_tian_gan_index = self.yue_zhu.tian_gan.index + 1
        if taiyuan_tian_gan_index > 9:
            taiyuan_tian_gan_index -= 10
        tiangan = tian_gan_list[taiyuan_tian_gan_index]
        taiyuan_dizhi_index = self.yue_zhu.di_zhi.index + 3
        if taiyuan_dizhi_index > 11:
            taiyuan_dizhi_index -= 12
        dizhi = di_zhi_list[taiyuan_dizhi_index]
        return JiaZi[tiangan + dizhi]

    def get_ming_gong(self):
        pass

    def get_shen_gong(self):
        pass

    def get_shen_sha(self):
        pass

    def get_xiao_yun(self):
        xiao_yun = XiaoYun(self.shi_zhu, self.gender, self.nian_zhu.tian_gan.yin_yang,
                           self.qi_yun_time.year - self.date.year + 1)
        result_list = xiao_yun.get_xiao_yun()
        result_ob = {}
        for item in result_list:
            print(item)
            result_ob[item.name] = item
        return result_list, result_ob

    def qi_yun_shi_jian(self):
        calculator = QiYunShiJian(self.date, self.gender, self.nian_zhu.tian_gan.yin_yang)
        return calculator.qi_yun_shi_jian
