from enum import Enum


class MingJuPosition(Enum):
    日干 = "ri_gan"
    日支 = "ri_zhi"
    时干 = "shi_gan"
    时支 = "shi_zhi"
    月干 = "yue_gan"
    月支 = "yue_zhi"
    年干 = "nian_gan"
    年支 = "nian_zhi"
    年令 = "nian_ling"
    月令 = "yue_ling"


class MingJuZhuPosition(Enum):
    日柱 = "ri_zhu"
    时柱 = "shi_zhu"
    月柱 = "yue_zhu"
    年柱 = "nian_zhu"
