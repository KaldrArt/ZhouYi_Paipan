from collections import namedtuple
from enum import Enum

RelationType = namedtuple("RelationType", ['name', 'score', 'effect', 'same_yin_yang'], defaults=['', 0, 0, 0])


class WuXingRelationType(Enum):
    生 = RelationType(name="生", score=30, effect=-1)
    克 = RelationType(name="克", score=20, effect=-1)
    被生 = RelationType(name="被生", score=30, effect=1)
    被克 = RelationType(name="被克", score=50, effect=-1)
    相同 = RelationType(name="相同", score=50, effect=1)


class TianGanDiZhiRelationType(Enum):
    生 = RelationType(name="生", score=30, effect=-1)
    克 = RelationType(name="克", score=20, effect=-1)
    被生 = RelationType(name="被生", score=50, effect=1)
    被克 = RelationType(name="被克", score=50, effect=-1)
    相同 = RelationType(name="相同", score=50, effect=1)
    同性生 = RelationType(name="同性生", score=20, effect=-1)
    异性生 = RelationType(name="异性生", score=15, effect=-1)
    同性克 = RelationType(name="同性克", score=20, effect=-1)
    异性克 = RelationType(name="异性克", score=15, effect=-1)
    同性被生 = RelationType(name="同性被生", score=50, effect=1)
    异性被生 = RelationType(name="异性被生", score=40, effect=1)
    同性被克 = RelationType(name="同性被克", score=50, effect=-1)
    异性被克 = RelationType(name="异性被克", score=40, effect=-1)
    同性相同 = RelationType(name="同性相同", score=50, effect=1)
    异性相同 = RelationType(name="异性相同", score=40, effect=1)
    冲 = RelationType(name="冲", score=50, effect=-1)
    刑 = RelationType(name="刑", score=20, effect=-1)
    自刑 = RelationType(name="自刑", score=20, effect=-1)
    同性刑 = RelationType(name="同性刑", score=20, effect=-1)
    异性刑 = RelationType(name="异性刑", score=15, effect=-1)
    害 = RelationType(name="害", score=10, effect=-1)
    合 = RelationType(name="合", score=30, effect=-1)
    同性半合 = RelationType(name="同性半合", score=10, effect=-1)
    异性半合 = RelationType(name="异性半合", score=5, effect=-1)
    同性半会 = RelationType(name="同性半会", score=10, effect=1)
    异性半会 = RelationType(name="异性半会", score=5, effect=1)
    半合 = RelationType(name="半合", score=10, effect=-1)
    半会 = RelationType(name="半会", score=10, effect=1)
    长生 = RelationType(name="长生")
    沐浴 = RelationType(name="沐浴")
    冠带 = RelationType(name="冠带")
    临官 = RelationType(name="临官")
    帝旺 = RelationType(name="帝旺")
    衰 = RelationType(name="衰")
    病 = RelationType(name="病")
    死 = RelationType(name="死")
    墓 = RelationType(name="墓")
    绝 = RelationType(name="绝")
    胎 = RelationType(name="胎")
    养 = RelationType(name="养")
    藏干本气 = RelationType(name="藏干本气", score=60, effect=1)
    藏干中气 = RelationType(name="藏干中气", score=30, effect=1)
    藏干余气 = RelationType(name="藏干余气", score=10, effect=1)
    藏干仅本气 = RelationType(name="藏干仅本气", score=100, effect=1)
    藏干其一本气 = RelationType(name="藏干其一本气", score=70, effect=1)
    藏干其二中气 = RelationType(name="藏干其二中气", score=30, effect=1)
