from bazi_common.wuxing import WuXing, wu_xing_list
from bazi_common.yi_base import YiBase, Yi
from bazi_common.zhangsheng import di_zhi_zhang_sheng, zhang_sheng_list

di_zhi_list = list("子丑寅卯辰巳午未申酉戌亥")

cang_gan = {
    "子": "癸",
    "丑": "己辛癸",
    "寅": "甲丙戊",
    "卯": "乙",
    "辰": "戊癸乙",
    "巳": "丙庚戊",
    "午": "丁己",
    "未": "己乙丁",
    "申": "庚壬戊",
    "酉": "辛",
    "戌": "戊丁辛",
    "亥": "壬甲"
}


class DiZhiBase(YiBase):
    def __init__(self, name):
        super().__init__(name)
        if name not in di_zhi_list:
            raise Exception("%s不是有效的地支" % name)
        self.wu_xing = self.get_wu_xing()
        self.zhang_sheng = {}
        self.cang_gan = {}

    def set_zhangsheng(self):
        zhang_sheng_dizhi_index = di_zhi_list.index(di_zhi_zhang_sheng[self.name])
        i = 0
        for item in zhang_sheng_list:
            item_dizhi_index = zhang_sheng_dizhi_index + i
            if item_dizhi_index >= 12:
                item_dizhi_index -= 12
            dizhi = di_zhi_list[item_dizhi_index]
            self.zhang_sheng[item] = DiZhi[dizhi]
            i += 1

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

    def get_zhangsheng(self):
        pass


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
