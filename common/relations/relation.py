from common.wuxing import WuXingBase
from common.yi_base import Yi
from common.zhangsheng import tian_gan_zhang_sheng, di_zhi_zhang_sheng, zhang_sheng_list
from common.tiangan import TianGan, tian_gan_list, TianGanBase
from common.dizhi import DiZhi, di_zhi_list, DiZhiBase
from common.relations.relation_type import *

shishen_map = {
    "同性相同": "比肩",
    "异性相同": "劫财",
    "同性生": "偏印",
    "异性生": "正印",
    "同性克": "偏官",
    "异性克": "正官",
    "同性被生": "食神",
    "异性被生": "伤官",
    "同性被克": "偏财",
    "异性被克": "正财",
    "克": "官杀",
    "被克": "财",
    "生": "印枭",
    "被生": "食伤",
    "相同": "比劫",
}


class Relation:
    def __init__(self, input1: Yi, input2: Yi):
        self.relations = {
            "with_yin_yang": [],
            "without_yin_yang": []
        }
        self.relation_names = []
        self.relation_names_with_yin_yang = []
        self.input1 = input1
        self.input2 = input2
        self.wu_xing_relation = None
        self.same_yin_yang = input1.value.yin_yang == input2.value.yin_yang
        self.wu_xing_relation: WuXingRelationType = WuXingRelationType.相同
        self.name = "%s == %s" % (input1.name, input2.name)
        self.get_relation()

    def get_relation(self):
        self.get_wu_xing_relation(self.input1.value.wu_xing.value, self.input2.value.wu_xing.value)
        self.get_sheng_ke()

    def get_shishen(self):
        pass

    def get_with_yin_yang_key(self, name):
        return "%s性%s" % ("同" if self.same_yin_yang else "异", name)

    def set_relation_names(self):
        for relation in self.relations['with_yin_yang']:
            self.relation_names_with_yin_yang.append(relation.name)
        for relation in self.relations['without_yin_yang']:
            self.relation_names.append(relation.name)

    def get_wu_xing_relation(self, wuxing1: WuXingBase, wuxing2: WuXingBase):
        diff = wuxing2.index - wuxing1.index
        if diff in [1, -4]:
            self.wu_xing_relation = WuXingRelationType.生
            self.name = "%s ==> %s" % (self.input1.name, self.input2.name)
        elif diff in [2, -3]:
            self.wu_xing_relation = WuXingRelationType.克
            self.name = "%s --> %s" % (self.input1.name, self.input2.name)
        elif diff in [3, -2]:
            self.wu_xing_relation = WuXingRelationType.被克
            self.name = "%s <-- %s" % (self.input1.name, self.input2.name)
        elif diff in [4, -1]:
            self.wu_xing_relation = WuXingRelationType.被生
            self.name = "%s <== %s" % (self.input1.name, self.input2.name)

    def get_sheng_ke(self):
        with_yin_yang_key = self.get_with_yin_yang_key(self.wu_xing_relation.name)
        shishen_without_yinyang = shishen_map[self.wu_xing_relation.name]
        shishen = shishen_map[with_yin_yang_key]
        relation_shishen = TianGanDiZhiRelationType[shishen]
        relation_shishen_without_yinyang = TianGanDiZhiRelationType[shishen_without_yinyang]
        self.relations['without_yin_yang'].append(TianGanDiZhiRelationType[self.wu_xing_relation.name])
        self.relations['without_yin_yang'].append(relation_shishen_without_yinyang)
        self.relations['without_yin_yang'].append(relation_shishen_without_yinyang)
        self.relations['with_yin_yang'].append(TianGanDiZhiRelationType[with_yin_yang_key])
        self.relations['with_yin_yang'].append(relation_shishen)
        self.relations['with_yin_yang'].append(relation_shishen_without_yinyang)
