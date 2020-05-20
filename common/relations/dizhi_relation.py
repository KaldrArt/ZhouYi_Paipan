from .relation import *


class DiZhiRelation(Relation):
    def __init__(self, dizhi1=DiZhi, dizhi2=DiZhi):
        self.dizhi1: DiZhiBase = dizhi1.value
        self.dizhi2: DiZhiBase = dizhi2.value
        super().__init__(dizhi1, dizhi2)

    def get_relation(self):
        """
        获取关系
        :return:
        """
        super().get_relation()
        # 冲
        self.get_chong()
        # 合
        self.get_he()
        # 刑
        self.get_xing()
        # 害
        self.get_hai()
        # 半合
        self.get_ban_he()
        # 半会
        self.get_ban_hui()

        self.set_relation_names()

    def get_chong(self):
        if self.dizhi1.index - self.dizhi2.index in [6, -6]:
            self.relations["with_yin_yang"].append(TianGanDiZhiRelationType.冲)
            self.relations["without_yin_yang"].append(TianGanDiZhiRelationType.冲)
            self.name = self.name.replace("==", "=冲=")
            self.name = self.name.replace("--", "-冲-")

    def get_hai(self):
        if self.dizhi1.index + self.dizhi2.index in [7, 19]:
            self.relations["with_yin_yang"].append(TianGanDiZhiRelationType.害)
            self.relations["without_yin_yang"].append(TianGanDiZhiRelationType.害)
            self.name = self.name.replace("==", "=害=")
            self.name = self.name.replace("--", "-害-")

    def get_he(self):
        if self.dizhi1.index + self.dizhi2.index in [1, 13]:
            self.relations["with_yin_yang"].append(TianGanDiZhiRelationType.合)
            self.relations["without_yin_yang"].append(TianGanDiZhiRelationType.合)
            self.name = self.name.replace("==", "=合=")
            self.name = self.name.replace("--", "-合-")

    def get_ban_he(self):
        index1 = self.dizhi1.index
        index2 = self.dizhi2.index
        if not index1 == index2:
            if (index1 % 4) == (index2 % 4):
                self.relations["with_yin_yang"].append(TianGanDiZhiRelationType[self.get_with_yin_yang_key('半合')])
                self.relations["without_yin_yang"].append(TianGanDiZhiRelationType.半合)

    def get_ban_hui(self):
        index1 = self.dizhi1.index - 2
        index2 = self.dizhi2.index - 2
        if index1 < 0:
            index1 += 12
        if index2 < 0:
            index2 += 12
        if not index1 == index2:
            if (index1 // 3) == (index2 // 3):
                self.relations["with_yin_yang"].append(TianGanDiZhiRelationType[self.get_with_yin_yang_key('半会')])
                self.relations["without_yin_yang"].append(TianGanDiZhiRelationType.半会)

    def get_xing(self):
        xing = False
        if self.dizhi1.name == self.dizhi2.name:
            if self.dizhi1.index % 3 == 0:
                xing = True
                self.relations["with_yin_yang"].append(TianGanDiZhiRelationType.自刑)
                self.relations["without_yin_yang"].append(TianGanDiZhiRelationType.自刑)
        else:
            xing_list = [['申', '巳', '寅'], ['丑', '戌', '未'], ['卯', '子']]
            for xing_item in xing_list:
                if self.input1.name in xing_item and self.input2.name in xing_item:
                    xing = True
                    with_yin_yang_key = self.get_with_yin_yang_key('刑')
                    self.relations["with_yin_yang"].append(TianGanDiZhiRelationType[with_yin_yang_key])
                    self.relations["without_yin_yang"].append(TianGanDiZhiRelationType.刑)
        if xing:
            self.name = self.name.replace("==", "=刑=")
            self.name = self.name.replace("--", "-刑-")
