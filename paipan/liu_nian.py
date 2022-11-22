from bazi_common.jiazi import JiaZi, JiaZiBase, jia_zi_list


def get_year_jia_zi(year):
    fix_year = 4  # 公元4年是甲子元年
    index = year % 60 - fix_year
    if index > 59:
        index -= 60
    elif index < 0:
        index += 60
    return jia_zi_list[index][0], jia_zi_list[index][1]


class LiuNian(JiaZiBase):
    def __init__(self, dayun, year, liu_nian_index, birth_year):
        self.year = year
        self.da_yun = dayun
        tiangan, dizhi = get_year_jia_zi(year)
        super().__init__(tiangan, dizhi, liu_nian_index)
        self.age = year - birth_year
   