from common.positions.position import Position, YiBase
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


PositionBase = namedtuple("PositionBase", [
    "name",
    "zhu",
    'score',
    "kong_wang",
    "di_zhi"
], defaults=[
    "", 1, None, False, False
])

xin_pai_gan_zhi_position_list = ['地支', '天干', '空亡地支', '月令', '年令', '大运天干', '大运地支', '空亡大运地支', '流年天干', '流年地支', '空亡流年地支',
                                 '小运天干', '小运地支']


class XinPaiGanZhiPosition(Enum):
    地支 = PositionBase('地支', XinPaiZhu.柱, 1, di_zhi=True)
    天干 = PositionBase('天干', XinPaiZhu.柱, 1)
    空亡地支 = PositionBase('空亡地支', XinPaiZhu.柱, -1, kong_wang=True, di_zhi=True)
    月令 = PositionBase('月令', XinPaiZhu.月柱, 5, di_zhi=True)
    年令 = PositionBase('年令', XinPaiZhu.年柱, 5, di_zhi=True)
    大运天干 = PositionBase("大运天干", XinPaiZhu.大运, 10)
    大运地支 = PositionBase("大运地支", XinPaiZhu.大运, 10, di_zhi=True)
    空亡大运地支 = PositionBase('空亡大运地支', XinPaiZhu.大运, -1, kong_wang=True, di_zhi=True)
    流年天干 = PositionBase('流年天干', XinPaiZhu.流年, 10)
    流年地支 = PositionBase('流年地支', XinPaiZhu.流年, 10, di_zhi=True)
    空亡流年地支 = PositionBase("空亡流年地支", XinPaiZhu.流年, -1, kong_wang=True, di_zhi=True)
    小运天干 = PositionBase("小运天干", XinPaiZhu.小运, 10)
    小运地支 = PositionBase('小运地支', XinPaiZhu.小运, 10, di_zhi=True)


class XinPaiGanZhi(Position):
    def __init__(self, yi: YiBase, position: XinPaiGanZhiPosition):
        self.yi = yi
        self.position = position
