from common.wuxing import WuXingBase
from common.yi_base import Yi
from common.tiangan import TianGan, tian_gan_list, TianGanBase
from common.dizhi import DiZhi, di_zhi_list, DiZhiBase
from common.relations.relation_type import *


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
        self.relations['without_yin_yang'].append(TianGanDiZhiRelationType[self.wu_xing_relation.name])
        self.relations['with_yin_yang'].append(TianGanDiZhiRelationType[with_yin_yang_key])
