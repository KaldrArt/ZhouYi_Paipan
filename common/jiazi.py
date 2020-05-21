from common.dizhi import DiZhi, di_zhi_list, DiZhiBase
from common.tiangan import TianGan, tian_gan_list, TianGanBase
from common.yi_base import Yi


def __generate_60_jia_zi():
    """
    生成60甲子
    :return:[
        '甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉',
        '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未',
        '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳',
        '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯',
        '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑',
        '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥'
    ]
    """
    x = 0
    result = []
    for k in range(5):
        for i in range(12):
            dizhi = DiZhi[di_zhi_list[i]].value.name
            tiangan = TianGan[tian_gan_list[x]].value.name
            result.append("%s%s" % (tiangan, dizhi))
            x += 1
            if x > 9:
                x -= 10
    return result


jia_zi_list = __generate_60_jia_zi()


class JiaZiBase:
    def __init__(self, tiangan: str, dizhi: str, index: int):
        self.tian_gan: TianGanBase = TianGan[tiangan].value
        self.di_zhi: DiZhiBase = DiZhi[dizhi].value
        self.name = self.tian_gan.name + self.di_zhi.name
        self.index = index
        self.xun, self.xun_index = self.get_xun()
        self.kong_wang = self.get_kong_wang()

    def get_xun(self) -> (str, int):
        xun_tian_gan_indexes = list("子戌申午辰寅")
        tian_gan_index = self.tian_gan.index
        xun_jia_dizhi_index = self.di_zhi.index - tian_gan_index
        if xun_jia_dizhi_index < 0:
            xun_jia_dizhi_index += 12
        dizhi = di_zhi_list[xun_jia_dizhi_index]
        xun_index = xun_tian_gan_indexes.index(dizhi)
        return "甲%s" % dizhi, xun_index

    def get_kong_wang(self) -> [DiZhiBase]:
        dizhi_index = di_zhi_list.index(self.xun[1])
        kongwang_dizhi_1 = dizhi_index - 2
        kongwang_dizhi_2 = dizhi_index - 1
        if kongwang_dizhi_1 < 0:
            kongwang_dizhi_1 += 12
        if kongwang_dizhi_2 < 0:
            kongwang_dizhi_2 += 12
        return [DiZhi[di_zhi_list[kongwang_dizhi_1]].value, DiZhi[di_zhi_list[kongwang_dizhi_2]].value]


class JiaZi(Yi):
    甲子 = JiaZiBase('甲', '子', 0)
    乙丑 = JiaZiBase('乙', '丑', 1)
    丙寅 = JiaZiBase('丙', '寅', 2)
    丁卯 = JiaZiBase('丁', '卯', 3)
    戊辰 = JiaZiBase('戊', '辰', 4)
    己巳 = JiaZiBase('己', '巳', 5)
    庚午 = JiaZiBase('庚', '午', 6)
    辛未 = JiaZiBase('辛', '未', 7)
    壬申 = JiaZiBase('壬', '申', 8)
    癸酉 = JiaZiBase('癸', '酉', 9)
    甲戌 = JiaZiBase('甲', '戌', 10)
    乙亥 = JiaZiBase('乙', '亥', 11)
    丙子 = JiaZiBase('丙', '子', 12)
    丁丑 = JiaZiBase('丁', '丑', 13)
    戊寅 = JiaZiBase('戊', '寅', 14)
    己卯 = JiaZiBase('己', '卯', 15)
    庚辰 = JiaZiBase('庚', '辰', 16)
    辛巳 = JiaZiBase('辛', '巳', 17)
    壬午 = JiaZiBase('壬', '午', 18)
    癸未 = JiaZiBase('癸', '未', 19)
    甲申 = JiaZiBase('甲', '申', 20)
    乙酉 = JiaZiBase('乙', '酉', 21)
    丙戌 = JiaZiBase('丙', '戌', 22)
    丁亥 = JiaZiBase('丁', '亥', 23)
    戊子 = JiaZiBase('戊', '子', 24)
    己丑 = JiaZiBase('己', '丑', 25)
    庚寅 = JiaZiBase('庚', '寅', 26)
    辛卯 = JiaZiBase('辛', '卯', 27)
    壬辰 = JiaZiBase('壬', '辰', 28)
    癸巳 = JiaZiBase('癸', '巳', 29)
    甲午 = JiaZiBase('甲', '午', 30)
    乙未 = JiaZiBase('乙', '未', 31)
    丙申 = JiaZiBase('丙', '申', 32)
    丁酉 = JiaZiBase('丁', '酉', 33)
    戊戌 = JiaZiBase('戊', '戌', 34)
    己亥 = JiaZiBase('己', '亥', 35)
    庚子 = JiaZiBase('庚', '子', 36)
    辛丑 = JiaZiBase('辛', '丑', 37)
    壬寅 = JiaZiBase('壬', '寅', 38)
    癸卯 = JiaZiBase('癸', '卯', 39)
    甲辰 = JiaZiBase('甲', '辰', 40)
    乙巳 = JiaZiBase('乙', '巳', 41)
    丙午 = JiaZiBase('丙', '午', 42)
    丁未 = JiaZiBase('丁', '未', 43)
    戊申 = JiaZiBase('戊', '申', 44)
    己酉 = JiaZiBase('己', '酉', 45)
    庚戌 = JiaZiBase('庚', '戌', 46)
    辛亥 = JiaZiBase('辛', '亥', 47)
    壬子 = JiaZiBase('壬', '子', 48)
    癸丑 = JiaZiBase('癸', '丑', 49)
    甲寅 = JiaZiBase('甲', '寅', 50)
    乙卯 = JiaZiBase('乙', '卯', 51)
    丙辰 = JiaZiBase('丙', '辰', 52)
    丁巳 = JiaZiBase('丁', '巳', 53)
    戊午 = JiaZiBase('戊', '午', 54)
    己未 = JiaZiBase('己', '未', 55)
    庚申 = JiaZiBase('庚', '申', 56)
    辛酉 = JiaZiBase('辛', '酉', 57)
    壬戌 = JiaZiBase('壬', '戌', 58)
    癸亥 = JiaZiBase('癸', '亥', 59)
