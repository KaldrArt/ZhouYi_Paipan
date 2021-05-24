from enum import Enum
from paipan.pai_pan import PaiPan
from paipan.position import Position

"""
规则

规则分为两种，一种是断语，将断语加到指定的地方，一种是分数，将算到的分数加到指定的地方
而无论是断语还是分数，都可以放在命局、六亲项目、流年、大运上。
"""


class RuleType(Enum):
    断语 = "断语"
    分数 = "分数"


class SubRuleType(Enum):
    命局 = "命局"
    命局神煞 = "命局神煞"
    六亲 = '六亲'
    流年 = '流年'
    流月 = "流月"
    流日 = "流日"
    大运 = '大运'
    命局大运 = "命局大运"
    命局流年 = "命局流年"
    命局流月 = "命局流月"
    命局流日 = "命局流日"
    六亲大运 = "六亲大运"
    六亲流年 = "六亲流年"
    六亲流月 = "六亲流月"
    六亲流日 = "六亲流日"


class Rule:
    def __init__(self, paipan: PaiPan,
                 analyzer_result,
                 target_position: Position = Position.日干,
                 effect_positions: [Position] = [Position.年干],
                 rule_types: [RuleType] = [RuleType.断语],
                 sub_rule_types: [SubRuleType] = [SubRuleType.命局]):
        self.paipan = paipan
        self.analyzer_result = analyzer_result
        self.target_position = target_position
        self.effect_positions = effect_positions
        self.rule_types = rule_types
        self.sub_rule_types = sub_rule_types
        self.run()

    def run(self):
        if RuleType.断语 in self.rule_types:
            for sub_type in self.sub_rule_types:
                self.calculate_text(sub_type)
        elif RuleType.分数 in self.rule_types:
            for sub_type in self.sub_rule_types:
                self.calculate_score(sub_type)

    def calculate_score(self, sub_rule_type: SubRuleType, result: dict = {}):
        if RuleType.分数.value not in self.analyzer_result:
            self.analyzer_result[RuleType.分数.value] = {}
        if sub_rule_type.value not in self.analyzer_result[RuleType.分数.value]:
            self.analyzer_result[RuleType.分数.value][sub_rule_type.value] = {}
        for key in result:
            if key not in self.analyzer_result[RuleType.分数.value][sub_rule_type.value]:
                self.analyzer_result[RuleType.分数.value][sub_rule_type.value][key] = 0
            self.analyzer_result[RuleType.分数.value][sub_rule_type.value][key] += result[key]

    def calculate_text(self, sub_rule_type: SubRuleType, result: dict = {}):
        if RuleType.断语.value not in self.analyzer_result:
            self.analyzer_result[RuleType.断语.value] = {}
        if sub_rule_type.value not in self.analyzer_result[RuleType.断语.value]:
            self.analyzer_result[RuleType.断语.value][sub_rule_type.value] = {}
        for key in result:
            if key not in self.analyzer_result[RuleType.断语.value][sub_rule_type.value]:
                self.analyzer_result[RuleType.断语.value][sub_rule_type.value][key] = []
            self.analyzer_result[RuleType.断语.value][sub_rule_type.value][key].append(result[key])
