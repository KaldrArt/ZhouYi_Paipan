from collections import namedtuple
from enum import Enum

Zhu = namedtuple(
    "Zhu", [
        "name",  # 名称
        'position',  # 位置
        "id",  # 编号
        'left',  # 左
        'right',  # 右
        'level'  # 级别
    ], defaults=['', -1, -1, -1, -1, -1]
)


class XinPaiZhu(Enum):
    时柱 = Zhu(name="时柱", position=3, id=3, left=2, right=1, level=1)
    日柱 = Zhu(name="日柱", position=2, id=2, left=1, right=3, level=1)
    月柱 = Zhu(name="月柱", position=1, id=1, left=0, right=2, level=1)
    年柱 = Zhu(name="年柱", position=0, id=0, left=2, right=1, level=1)
    大运 = Zhu(name="大运", position=4, id=4, left=-1, right=-1, level=2)
    流年 = Zhu(name="流年", position=5, id=5, left=-1, right=-1, level=2)
    小运 = Zhu(name="小运", position=7, id=7, left=-1, right=-1, level=3)
    柱 = Zhu(name="柱", position=6, id=6, left=-1, right=-1, level=1)


Position = namedtuple("Position", [
    "name",
    "zhu",
    'score',
    "kong_wang",
    "di_zhi"
], defaults=[
    "", 1, None, False, False
])


class XinPaiEffectGanZhiPosition(Enum):
    地支 = Position('地支', XinPaiZhu.柱, 1, di_zhi=True)
    天干 = Position('天干', XinPaiZhu.柱, 1)
    空亡地支 = Position('空亡地支', XinPaiZhu.柱, -1, kong_wang=True, di_zhi=True)
    月令 = Position('月令', XinPaiZhu.月柱, 5, di_zhi=True)
    年令 = Position('年令', XinPaiZhu.年柱, 5, di_zhi=True)
    大运天干 = Position("大运天干", XinPaiZhu.大运, 10)
    大运地支 = Position("大运地支", XinPaiZhu.大运, 10, di_zhi=True)
    空亡大运地支 = Position('空亡大运地支', XinPaiZhu.大运, -1, kong_wang=True, di_zhi=True)
    流年天干 = Position('流年天干', XinPaiZhu.流年, 10)
    流年地支 = Position('流年地支', XinPaiZhu.流年, 10, di_zhi=True)
    空亡流年地支 = Position("空亡流年地支", XinPaiZhu.流年, -1, kong_wang=True, di_zhi=True)
    小运天干 = Position("小运天干", XinPaiZhu.小运, 10)
    小运地支 = Position('小运地支', XinPaiZhu.小运, 10, di_zhi=True)


XinPaiRelationType = namedtuple("RelationType", [
    'name',
    'score',
    'effect',
    "position",
    'same_yin_yang',
    'normal_relations'
], defaults=['', 0, 0, None, False, []])
