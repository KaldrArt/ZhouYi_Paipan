from common.wuxing import WuXing, wu_xing_list
from common.yi_base import YiBase, Yi
from common.zhangsheng import tian_gan_zhang_sheng, zhang_sheng_list
from common.dizhi import di_zhi_list, DiZhi

tian_gan_list = list("甲乙丙丁戊己庚辛壬癸")


class TianGanBase(YiBase):
    def __init__(self, name):
        super().__init__(name)
        if name not in tian_gan_list:
            raise Exception("%s不是有效的天干" % name)
        self.wu_xing = WuXing[wu_xing_list[tian_gan_list.index(name) // 2]]
        self.zhang_sheng = {}
        self.shi_shen_relation = {}
        self.set_zhangsheng()

    def set_shi_shen_relation(self):
        pass

    def set_zhangsheng(self):
        zhang_sheng_dizhi_index = di_zhi_list.index(tian_gan_zhang_sheng[self.name])
        i = 0
        for item in zhang_sheng_list:
            if self.yin_yang:
                item_dizhi_index = zhang_sheng_dizhi_index + i
            else:
                item_dizhi_index = zhang_sheng_dizhi_index - i
            if item_dizhi_index >= 12:
                item_dizhi_index -= 12
            elif item_dizhi_index < 0:
                item_dizhi_index += 12
            dizhi = di_zhi_list[item_dizhi_index]
            self.zhang_sheng[item] = DiZhi[dizhi]
            i += 1


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
