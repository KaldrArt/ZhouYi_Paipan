from bazi_common.dizhi import DiZhiBase, Yi
from bazi_common import *

liu_qin_list = "兄孙财官父"
wu_xing_list = '木火土金水'



class DaZongYi(Yi):
    pass


class DaZongYiLiuYaoDiZhiBase(DiZhiBase):
    def get_liu_qin_to_wu_xing(self, wu_xing):
        target_wu_xing_index = wu_xing_list.find(wu_xing)
        current_wu_xing_index = wu_xing_list.find(self.wu_xing.name)
        return liu_qin_list[current_wu_xing_index - target_wu_xing_index]


class DiZhi(DaZongYi):
    子 = DaZongYiLiuYaoDiZhiBase('子')
    丑 = DaZongYiLiuYaoDiZhiBase('丑')
    寅 = DaZongYiLiuYaoDiZhiBase('寅')
    卯 = DaZongYiLiuYaoDiZhiBase('卯')
    辰 = DaZongYiLiuYaoDiZhiBase('辰')
    巳 = DaZongYiLiuYaoDiZhiBase('巳')
    午 = DaZongYiLiuYaoDiZhiBase('午')
    未 = DaZongYiLiuYaoDiZhiBase('未')
    申 = DaZongYiLiuYaoDiZhiBase('申')
    酉 = DaZongYiLiuYaoDiZhiBase('酉')
    戌 = DaZongYiLiuYaoDiZhiBase('戌')
    亥 = DaZongYiLiuYaoDiZhiBase('亥')
