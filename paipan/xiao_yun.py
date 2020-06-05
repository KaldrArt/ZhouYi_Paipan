from common import *


class XiaoYun:
    def __init__(self, shi_zhu: JiaZiBase, gender=True, nian_gan_yin_yang=True, count=15):
        self.shi_zhu = shi_zhu
        self.gender = gender
        self.nian_gan_yin_yang = nian_gan_yin_yang
        self.count = count

    def get_xiao_yun(self):
        shi_zhu_index = self.shi_zhu.index
        if self.gender == self.nian_gan_yin_yang:
            start = shi_zhu_index + 1
            end = shi_zhu_index + self.count + 1
            factor = 1
        else:
            end = shi_zhu_index - self.count - 1
            start = shi_zhu_index - 1
            factor = -1
        if start < 0 or start > 59:
            start -= 60
        if end < 0 or end > 59:
            end -= 60
        return [JiaZi[x].value for x in jia_zi_list[start:end:factor]]
