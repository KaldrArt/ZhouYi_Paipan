from .ge_ju import GeJuBase, GeJu
from paipan import *
from enum import Enum


class TianGanShengYuYueLingWangRuo(Enum):
    旺 = "旺"
    弱 = "弱"
    不旺不弱 = "不旺不弱"


class GeJuAnalyzer:
    """
    格局分析


    """

    def __init__(self, pai_pan: PaiPan, liu_qin_relation=LiuQinBasic):
        self.pai_pan = pai_pan
        self.liu_qin_relation = liu_qin_relation
        self.yue_ling_kong_wang = self.check_yue_ling_kong_wang()
        self.yue_ling_shou_zhi_twice = self.check_yue_ling_shou_zhi_twice()

    def check_zhu_you_li(self):
        pass

    def check_yue_ling_kong_wang(self):
        yue_ling = self.pai_pan.yue_zhu.di_zhi
        if yue_ling.name in [x.name for x in self.pai_pan.kong_wang]:
            return True
        else:
            return False

    def check_yue_ling_shou_zhi_twice(self):
        pass

    def check_tian_gan_sheng_yu_yue_ling_wang_ruo(self):
        
        pass
