from enum import Enum
from collections import namedtuple

DaYunLiuNianPositionBase = namedtuple("DaYunLiuNianPositionBase", [
    'name', 'zhu', 'score'
], defaults=['', None, 2])


class DaYunLiuNianZhuPosition(Enum):
    大运 = "大运"
    流年 = "流年"
    小运 = "小运"


da_yun_liu_nian_position_list = ['大运天干', "大运地支", "流年天干", "流年地支", "小运天干", "小运地支"]


class DaYunLiuNianPosition(Enum):
    大运天干 = DaYunLiuNianPositionBase("大运天干", DaYunLiuNianZhuPosition.大运)
    大运地支 = DaYunLiuNianPositionBase("大运地支", DaYunLiuNianZhuPosition.大运)
    流年天干 = DaYunLiuNianPositionBase("流年天干", DaYunLiuNianZhuPosition.流年)
    流年地支 = DaYunLiuNianPositionBase("流年地支", DaYunLiuNianZhuPosition.流年)
    小运天干 = DaYunLiuNianPositionBase("小运天干", DaYunLiuNianZhuPosition.小运)
    小运地支 = DaYunLiuNianPositionBase("小运地支", DaYunLiuNianZhuPosition.小运)
