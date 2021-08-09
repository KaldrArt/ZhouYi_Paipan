from enum import Enum


class GeJuBase:
    """
        格局分析的是八字本身，在不掺和大运流年的情况下，八字本身涵盖的信息。
        一个八字，一个格局。
        给定了八字，应该去分析这个八字对应的格局是什么。从格局中直接判断八字中涵盖的六亲的关系。
        格局的下一步是内外左右环境论。
        在下一步是虚实论和大运流年论。
        格局中，应当包含每个六亲的用忌情况。
    """

    def __init__(self, name="", wang=True, cong=True):
        self.name = name
        self.wang = wang
        self.cong = cong
        self.yong_shen = self.set_yong_ji()

    def set_yong_ji(self):
        yong_shen = {
            "zheng_guan": False,
            "pian_guan": False,
            "zheng_cai": False,
            "pian_cai": False,
            "shang_guan": False,
            "shi_shen": False,
            "zheng_yin": True,
            "pian_yin": True,
            "bi_jian": True,
            "jie_cai": True
        }
        if (self.wang and not self.cong) or (not self.wang and self.cong):
            """
            身旺和从弱格局的用神一样
            """
            for liu_qin in yong_shen:
                yong_shen[liu_qin] = not yong_shen[liu_qin]
        return yong_shen


class GeJu(Enum):
    身旺 = GeJuBase("身旺", True, False)
    身弱 = GeJuBase("身弱", False, False)
    从旺 = GeJuBase("从旺", True, True)
    从弱 = GeJuBase("从弱", False, True)
