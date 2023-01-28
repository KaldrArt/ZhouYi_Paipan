from bazi_common.jiazi import JiaZi, JiaZiBase, jia_zi_list
from paipan.liu_nian import LiuNian


class DaYunDetail(JiaZiBase):
    def __init__(self, year, tiangan: str, dizhi: str, index: int, birth_year):
        super().__init__(tiangan, dizhi, index)
        self.start_year = year
        self.end_year = year + 9
        self.birth_year = birth_year
        self.start_age = year - birth_year
        self.end_age = self.end_year - birth_year
        self.liu_nian_list = []
        self.liu_nian_ob = {}
        self.generate_liu_nians()

    def generate_liu_nians(self):
        for i in range(10):
            year = self.start_year + i
            liu_nian = LiuNian(self, year, i, self.birth_year)
            self.liu_nian_list.append(liu_nian)
            self.liu_nian_ob[liu_nian.name] = liu_nian


class DaYun:
    def __init__(self, yue_zhu: JiaZiBase, nianzhu_yinyang, start_year, birth_year, gender=True, count=10):
        """
        根据八字信息生成大运
        :param yue_zhu:八字月柱
        :param nianzhu_yinyang:年柱天干的阴阳
        :param start_year: 第一个大运开始的时间
        :param gender: 性别
        :param count: 大运数量
        """
        self.count = count
        self.da_yun_list = []
        self.da_yun_ob = {}
        self.liu_nian_list = []
        self.liu_nian_ob = {}
        self.birth_year = birth_year
        self.yue_zhu = yue_zhu
        self.nianzhu_yinyang = nianzhu_yinyang
        self.start_year = start_year
        self.gender = gender
        self.generate_da_yuns()
        self.generate_liu_nians()

    def generate_da_yuns(self):
        factor = -1  # 男命生于阴年，女命生于阳年
        if (self.gender and self.nianzhu_yinyang) or (not self.gender and not self.nianzhu_yinyang):
            """
            男命生于阳年，女命生于阴年
            """
            factor = 1
        start_index = self.yue_zhu.index
        for i in range(self.count):
            index = start_index + factor * (i + 1)
            if index > 59:
                index -= 60
            elif index < 0:
                index += 60
            jia_zi_name = jia_zi_list[index]
            dayun_start_year = self.start_year + i * 10
            dayun = DaYunDetail(dayun_start_year, jia_zi_name[0], jia_zi_name[1], i, self.birth_year)
            self.da_yun_list.append(dayun)
            self.da_yun_ob[jia_zi_name] = dayun

    def generate_liu_nians(self):
        for dayun_name in self.da_yun_ob:
            liu_nian_ob = self.da_yun_ob[dayun_name].liu_nian_ob
            for liu_nian_name in liu_nian_ob:
                self.liu_nian_list.append(liu_nian_ob[liu_nian_name])
                if dayun_name not in self.liu_nian_ob:
                    self.liu_nian_ob[dayun_name] = {}
                self.liu_nian_ob[dayun_name][liu_nian_name] = liu_nian_ob[liu_nian_name]

    def print_dayun_liunian_table(self):
        pass


dy = DaYun(JiaZi.庚戌.value, False, 1989, 1987)
