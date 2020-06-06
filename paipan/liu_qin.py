from enum import Enum
from common import *
from paipan.pai_pan import PaiPan

liu_qin_list = ["偏印", "正印",
                "偏官", "正官",
                "食神", "伤官",
                "偏财", "正财",
                "比肩", "劫财"]


class LiuQinType(Enum):
    偏印 = "偏印"
    正印 = "正印"
    偏官 = "偏官"
    正官 = "正官"
    食神 = "食神"
    伤官 = "伤官"
    偏财 = "偏财"
    正财 = "正财"
    比肩 = "比肩"
    劫财 = "劫财"


class LiuQin:
    def __init__(self, base_gan: TianGanBase, effect_gan: TianGanBase):
        self.base_gan = base_gan
        self.effect_gan = effect_gan
        self.yong_shen = False
        self.tou = False

    def set_tou(self, tou=False):
        self.tou = tou

    def set_yong_shen(self, yong_shen=False):
        self.yong_shen = yong_shen


class LiuQinRelation:
    def __init__(self, pai_pan: PaiPan):
        pass
