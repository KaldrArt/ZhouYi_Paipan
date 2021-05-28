from enum import Enum
from paipan.pai_pan import PaiPan
from paipan.position import Position

"""
规则

规则分为两种，一种是断语，将断语加到指定的地方，一种是分数，将算到的分数加到指定的地方
而无论是断语还是分数，都可以放在命局、六亲项目、流年、大运上。

运算规则：

1. 搜索组合Search：从命局和大运里面找符合条件的内容，例如组成了三合局、三会局、神煞
    1.1 不指定目标位置，全局搜索，找三合局、三会局
    1.2 指定一个目标位置，搜索其他符合条件的作用位置，例如找神煞、找日干的三合水局
    1.3 指定多个目标位置，搜索其他符合条件的作用位置，例如找通关
    
    1.1~1.3包含：
        找relation，包括各种关系
        找name，例如，例如从命局、大运、流年中effect中找到“申子辰”即可
        找cang_gan，从effect中找到
        找zhang_sheng，从effect中找到某个长生

2. 计算分数
    2.1 旺衰的计算
    2.2 格局的计算
"""


class RuleType(Enum):
    """
    两种类型，一种是最终生成断语，一种是生成分数
    """
    断语 = "断语"
    分数 = "分数"


class SubRuleType(Enum):
    """
    子类型，将断语和分数放到哪个分类里
    """
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
    def __init__(self,
                 name,
                 paipan: PaiPan,
                 analyzer_result,
                 target_positions: [Position] = [Position.日干],  # 目标干支或柱的位置
                 effect_positions: [Position] = [Position.年干],  # 作用干支或柱的位置
                 rule_types: [RuleType] = [RuleType.断语],
                 sub_rule_types: [SubRuleType] = [SubRuleType.命局]
                 ):
        self.name = name
        self.paipan = paipan
        self.analyzer_result = analyzer_result
        self.target_positions = target_positions
        self.effect_positions = effect_positions
        self.rule_types = rule_types
        self.sub_rule_types = sub_rule_types
        self.result = {}
        self.run()

    def calculate_fuc(self):
        pass

    def calculate_result(self, preset_result={}):
        self.result = preset_result
        return preset_result

    def build_targets_cause(self, targets, relation):
        pass

    def build_cause(self, target, effects, relation):
        return {
            "position": "",
            "relations": []
        }

    def run(self):
        result = self.calculate_result()
        if RuleType.断语 in self.rule_types:
            for sub_type in self.sub_rule_types:
                self.calculate_text(sub_type, result)
        elif RuleType.分数 in self.rule_types:
            for sub_type in self.sub_rule_types:
                self.calculate_score(sub_type, result)

    def calculate_score(self, sub_rule_type: SubRuleType, result: dict = {}):
        if RuleType.分数.value not in self.analyzer_result:
            self.analyzer_result[RuleType.分数.value] = {}
        if sub_rule_type.value not in self.analyzer_result[RuleType.分数.value]:
            self.analyzer_result[RuleType.分数.value][sub_rule_type.value] = {}
        for key in result:
            if key not in self.analyzer_result[RuleType.分数.value][sub_rule_type.value]:
                self.analyzer_result[RuleType.分数.value][sub_rule_type.value][key] = {"rule_name": self.name, "value": 0,
                                                                                     'cause': result[key]['cause']}
            self.analyzer_result[RuleType.分数.value][sub_rule_type.value][key]['value'] += result[key]['value']

    def calculate_text(self, sub_rule_type: SubRuleType, result: dict = {}):
        if RuleType.断语.value not in self.analyzer_result:
            self.analyzer_result[RuleType.断语.value] = {}
        if sub_rule_type.value not in self.analyzer_result[RuleType.断语.value]:
            self.analyzer_result[RuleType.断语.value][sub_rule_type.value] = {}
        for key in result:
            if key not in self.analyzer_result[RuleType.断语.value][sub_rule_type.value]:
                self.analyzer_result[RuleType.断语.value][sub_rule_type.value][key] = {"rule_name": self.name,
                                                                                     "value": [],
                                                                                     'cause': result[key]['cause']}
            self.analyzer_result[RuleType.断语.value][sub_rule_type.value][key]['value'].append(result[key]['text'])


class SearchRule(Rule):
    def __init__(self, name,
                 paipan: PaiPan,
                 analyzer_result,
                 target_positions: [Position] = [Position.日干],  # 目标干支或柱的位置
                 effect_positions: [Position] = [Position.年干],  # 作用干支或柱的位置
                 rule_types: [RuleType] = [RuleType.断语],
                 sub_rule_types: [SubRuleType] = [SubRuleType.命局],
                 search_pattern={},
                 ):
        super(SearchRule, self).__init__(
            name,
            paipan,
            analyzer_result,
            target_positions,
            effect_positions,
            rule_types,
            sub_rule_types
        )

    def only_search_effect_positions(self):
        pass
