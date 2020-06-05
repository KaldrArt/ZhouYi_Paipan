from .relation import *

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
    "异性被克": "正财"
}


class TianGanRelation(Relation):
    def __init__(self, tiangan1: TianGan, tiangan2: TianGan):
        self.tiangan1 = tiangan1.value
        self.tiangan2 = tiangan2.value
        self.shi_shen = None
        super().__init__(tiangan1, tiangan2)

    def get_shi_shen_relation(self):
        for r in self.relations['with_yin_yang']:
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
