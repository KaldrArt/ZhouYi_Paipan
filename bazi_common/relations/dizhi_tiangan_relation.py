from bazi_common.relations.relation import *
from bazi_common.dizhi import cang_gan


class DiZhiTianGanRelation(Relation):
    def __init__(self, dizhi: DiZhi, tiangan: TianGan):
        self.tiangan: TianGanBase = tiangan.value
        self.dizhi: DiZhiBase = dizhi.value
        super().__init__(dizhi, tiangan)
        self.get_cang_gan()
        self.get_zhangsheng()

    def get_zhangsheng(self):
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
