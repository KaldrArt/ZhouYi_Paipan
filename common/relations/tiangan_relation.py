from .relation import *


class TianGanRelation(Relation):
    def __init__(self, tiangan1: TianGan, tiangan2: TianGan):
        self.tiangan1 = tiangan1.value
        self.tiangan2 = tiangan2.value
        self.shi_shen = None
        super().__init__(tiangan1, tiangan2)

    def get_shi_shen_relation(self):
        for r in self.relations['with_yin_yang']:
            if r.name in shishen_map:
                new_type = shishen_map[r.name]
                self.shi_shen = TianGanDiZhiRelationType[new_type]

    def get_relation(self):
        super().get_relation()
        self.get_shi_shen_relation()
        self.get_chong()
        self.get_he()
        self.set_relation_names()

    def get_chong(self):
        pass

    def get_he(self):
        index1 = self.tiangan1.index
        index2 = self.tiangan2.index
        if index1 - index2 in [5, -5]:
            self.relations["with_yin_yang"].append(TianGanDiZhiRelationType.合)
            self.relations["without_yin_yang"].append(TianGanDiZhiRelationType.合)
            self.name = self.name.replace("==", "=合=")
            self.name = self.name.replace("--", "-合-")
