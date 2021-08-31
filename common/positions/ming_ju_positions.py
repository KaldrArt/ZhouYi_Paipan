from enum import Enum
from collections import namedtuple

ming_ju_zhu_position_list = ['日柱', '月柱', '时柱', '年柱']
ming_ju_position_list = ["日干", '日支', '时干', '时支', '月干', '月支', '年干', '年支', '月令', '年令']
MingJuPositionBase = namedtuple("MingJuPositionBase", [
    'name', 'zhu', 'score'
], defaults=['', None, 2])


class MingJuZhuPosition(Enum):
    日柱 = "日柱"
    时柱 = "时柱"
    月柱 = "月柱"
    年柱 = "年柱"


class MingJuPosition(Enum):
    日干 = MingJuPositionBase("日干", MingJuZhuPosition.日柱)
    日支 = MingJuPositionBase("日支", MingJuZhuPosition.月柱)
    时干 = MingJuPositionBase("时干", MingJuZhuPosition.时柱)
    时支 = MingJuPositionBase("时支", MingJuZhuPosition.时柱)
    月干 = MingJuPositionBase("月干", MingJuZhuPosition.月柱)
    月支 = MingJuPositionBase("月支", MingJuZhuPosition.月柱)
    年干 = MingJuPositionBase("年干", MingJuZhuPosition.年柱)
    年支 = MingJuPositionBase("年支", MingJuZhuPosition.年柱)
    年令 = MingJuPositionBase("年令", MingJuZhuPosition.年柱)
    月令 = MingJuPositionBase("月令", MingJuZhuPosition.月柱)
