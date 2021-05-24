from enum import Enum
from paipan.pai_pan import PaiPan

"""
规则

规则分为两种，一种是断语，将断语加到指定的地方，一种是分数，将算到的分数加到指定的地方
"""


class RuleType(Enum):
    断语 = "断语"
    分数 = "分数"


class Rule:
    def __init__(self, paipan: PaiPan, target_position="日干", effect_positions=[], rule_type=RuleType):
        self.paipan = paipan
        self.target_position = target_position
        self.effect_positions = effect_positions
        self.rule_type = ""

    def run(self):
        pass
