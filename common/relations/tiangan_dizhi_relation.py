from common.relations.relation import *
from common.zhangsheng import tian_gan_zhang_sheng, zhang_sheng_list

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


class TianGanDiZhiRelation(Relation):
    def __init__(self, tiangan: TianGan, dizhi: DiZhi):
        self.tiangan: TianGanBase = tiangan.value
        self.dizhi: DiZhiBase = dizhi.value
        super().__init__(tiangan, dizhi)

    def get_relation(self):
        super().get_relation()
        self.get_zhang_sheng()
        self.get_cang_gan()
        self.set_relation_names()

    def get_cang_gan(self):

        tiangans = list(cang_gan[self.dizhi.name])
        if self.tiangan.name in tiangans:
            if len(tiangans) == 1:
                self.relations["with_yin_yang"].append(TianGanDiZhiRelationType.藏干仅本气)
                self.relations["without_yin_yang"].append(TianGanDiZhiRelationType.藏干仅本气)
            elif len(tiangans) == 2:
                if tiangans.index(self.tiangan.name) == 0:
                    self.relations["with_yin_yang"].append(TianGanDiZhiRelationType.藏干其一本气)
                    self.relations["without_yin_yang"].append(TianGanDiZhiRelationType.藏干其一本气)
                else:
                    self.relations["with_yin_yang"].append(TianGanDiZhiRelationType.藏干其二中气)
                    self.relations["without_yin_yang"].append(TianGanDiZhiRelationType.藏干其二中气)
            else:
                if tiangans.index(self.tiangan.name) == 0:
                    self.relations["with_yin_yang"].append(TianGanDiZhiRelationType.藏干本气)
                    self.relations["without_yin_yang"].append(TianGanDiZhiRelationType.藏干本气)
                elif tiangans.index(self.tiangan.name) == 1:
                    self.relations["with_yin_yang"].append(TianGanDiZhiRelationType.藏干中气)
                    self.relations["without_yin_yang"].append(TianGanDiZhiRelationType.藏干中气)
                else:
                    self.relations["with_yin_yang"].append(TianGanDiZhiRelationType.藏干余气)
                    self.relations["without_yin_yang"].append(TianGanDiZhiRelationType.藏干余气)

    def get_zhang_sheng(self):
        zhang_sheng_di_zhi_name = tian_gan_zhang_sheng[self.tiangan.name]
        tian_gan_yin_yang = self.tiangan.yin_yang
        zhang_sheng_di_zhi_position = DiZhi[zhang_sheng_di_zhi_name].value.index
        di_zhi_position = self.dizhi.index
        if tian_gan_yin_yang:
            zhang_sheng_index = di_zhi_position - zhang_sheng_di_zhi_position
        else:
            zhang_sheng_index = zhang_sheng_di_zhi_position - di_zhi_position
        if zhang_sheng_index < 0:
            zhang_sheng_index += 12  # 一定是一个0-11的正整数
        zhang_sheng_name = zhang_sheng_list[zhang_sheng_index]
        self.relations["with_yin_yang"].append(TianGanDiZhiRelationType[zhang_sheng_name])
        self.relations["without_yin_yang"].append(TianGanDiZhiRelationType[zhang_sheng_name])
