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
    1.1 月令空亡
        生于年令，根据年令对日干的作用断旺衰
        1.1.1 旺
        1.1.2 弱
        1.1.3 不旺也不弱
            根据月干对日干的作用断旺衰
            TODO: 根据年干对日干的作用断旺衰，并且
    1.2 月令不空
        1.2.1 月令受制2次
            1.2.1.1 日支没有受制2次
                1.2.1.1.1 年支和日支对日主作用相同
                    根据作用来断旺衰，同旺则身旺，同弱则身弱
                1.2.1.1.2 年支和日支对日主的作用不同
                    根据1.2.2来断
            1.2.1.2 日支受制2次
                根据1.2.2来断
        1.2.2 月令没有受制2次
            生于月令，根据月令对日干的作用断旺衰
            1.2.2.1 旺
            1.2.2.2 弱
            1.2.2.3 不旺也不弱
                根据月干对日干的作用断旺衰
    """

    def __init__(self, pai_pan: PaiPan, liu_qin_relation=LiuQinBasic):
        self.pai_pan = pai_pan
        self.liu_qin_relation = liu_qin_relation
        self.yue_ling_kong_wang = self.check_yue_ling_kong_wang()
        if self.yue_ling_kong_wang:
            pass
        else:
            pass
        self.yue_ling_shou_zhi_twice = self.check_yue_ling_shou_zhi_twice()

    def check_gan_you_li(self, target_gan=""):
        pass

    def check_zhu_you_li(self, from_ling="yue_ling") -> TianGanShengYuYueLingWangRuo:
        target = "ri_gan"
        if from_ling == "yue_ling":
            pass
        elif from_ling == "nian_ling":
            pass
        elif from_ling == "yue_gan":
            pass
        elif from_ling == "nian_gan":
            pass
        else:
            raise ("只能从月令、年令、月干、年干取")

    def check_yue_ling_kong_wang(self):
        """
        检查月令是否空亡
        """
        yue_ling = self.pai_pan.yue_zhu.di_zhi
        if yue_ling.name in [x.name for x in self.pai_pan.kong_wang]:
            return True
        else:
            return False

    def check_yue_ling_shou_zhi_twice(self):
        pass

    def check_tian_gan_sheng_yu_yue_ling_wang_ruo(self):

        pass
