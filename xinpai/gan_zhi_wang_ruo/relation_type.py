from collections import namedtuple

XinPaiRelationType = namedtuple("RelationType", [
    'name',
    'score',
    'effect',
    "position",
    'same_yin_yang',
    'normal_relations'
], defaults=['', 0, 0, None, False, []])
