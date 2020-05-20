from enum import Enum
from common.wuxing import WuXing, wu_xing_list
from common.yi_base import YiBase, Yi

tian_gan_list = list("甲乙丙丁戊己庚辛壬癸")


class TianGanBase(YiBase):
    def __init__(self, name):
        super().__init__(name)
        if name not in tian_gan_list:
            raise Exception("%s不是有效的天干" % name)
        self.wu_xing = WuXing[wu_xing_list[tian_gan_list.index(name) // 2]]


class TianGan(Yi):
    甲 = TianGanBase('甲')
    乙 = TianGanBase('乙')
    丙 = TianGanBase('丙')
    丁 = TianGanBase('丁')
    戊 = TianGanBase('戊')
    己 = TianGanBase('己')
    庚 = TianGanBase('庚')
    辛 = TianGanBase('辛')
    壬 = TianGanBase('壬')
    癸 = TianGanBase('癸')
