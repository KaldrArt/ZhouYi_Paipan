from enum import Enum

chars = list('甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥')


def generate_relation_map():
    result = {}
    for char in chars:
        result[char] = []
    return result


class YiBase:
    def __init__(self, name):
        self.name = name
        if name not in chars:
            raise Exception("%s不是有效的字符" % name)
        self.index = chars.index(name)
        if self.index > 9:
            self.index -= 10
        self.yin_yang = False if chars.index(name) % 2 else True
        self.relations = generate_relation_map()
        self.relations_with_yin_yang = generate_relation_map()


class Yi(Enum):
    pass
