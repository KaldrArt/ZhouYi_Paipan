from enum import Enum
from common.wuxing import WuXing, wu_xing_list
from common.yi_base import YiBase, Yi

di_zhi_list = list("子丑寅卯辰巳午未申酉戌亥")


class DiZhiBase(YiBase):
    def __init__(self, name):
        super().__init__(name)
        if name not in di_zhi_list:
            raise Exception("%s不是有效的地支" % name)
        self.wu_xing = self.get_wu_xing()

    def get_wu_xing(self) -> WuXing:
        index = di_zhi_list.index(self.name) - 2
        if index < 0:
            index += 12
        if (index + 1) % 3 == 0:
            wu_xing_index = 2
        else:
            wu_xing_index = index // 3
            if wu_xing_index > 1:
                wu_xing_index += 1
        return WuXing[wu_xing_list[wu_xing_index]]


class DiZhi(Yi):
    子 = DiZhiBase('子')
    丑 = DiZhiBase('丑')
    寅 = DiZhiBase('寅')
    卯 = DiZhiBase('卯')
    辰 = DiZhiBase('辰')
    巳 = DiZhiBase('巳')
    午 = DiZhiBase('午')
    未 = DiZhiBase('未')
    申 = DiZhiBase('申')
    酉 = DiZhiBase('酉')
    戌 = DiZhiBase('戌')
    亥 = DiZhiBase('亥')
