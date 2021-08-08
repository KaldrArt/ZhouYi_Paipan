from enum import Enum

formal_liu_qin_list = ["正官", "偏官", '正财', '偏财', '正印', '偏印', '食神', '伤官', '比肩', '劫财']


class LiuQinBase:
    def __init__(self, name=""):
        if name not in formal_liu_qin_list:
            raise "六亲必须在正规六亲列表中"
        self.name = name


class LiuQin(Enum):
    正官 = LiuQinBase('正官')
    官 = LiuQinBase("正官")
    偏官 = LiuQinBase("偏官")
    七杀 = LiuQinBase("偏官")
    鬼 = LiuQinBase("偏官")
    杀 = LiuQinBase("偏官")
    正财 = LiuQinBase("正财")
    财 = LiuQinBase("正财")
    偏财 = LiuQinBase("偏财")
    才 = LiuQinBase("偏财")
    正印 = LiuQinBase("正印")
    印 = LiuQinBase("正印")
    偏印 = LiuQinBase("偏印")
    枭 = LiuQinBase("偏印")
    比肩 = LiuQinBase("比肩")
    比 = LiuQinBase("比肩")
    劫财 = LiuQinBase("劫财")
    劫 = LiuQinBase("劫财")
    食神 = LiuQinBase("食神")
    食 = LiuQinBase("食神")
    伤官 = LiuQinBase("伤官")
    伤 = LiuQinBase("伤官")


class LiuQinNetwork:
    def __init__(self, base_liu_qin: LiuQin, target_liuqin: LiuQin):
        """
        获取原八字中，某个六亲的其他六亲
        """
        pass


class SocietyNetwork:
    male = ['爸爸', '爷爷', '外公', '舅舅', '弟弟', '哥哥', '叔叔', '伯伯']
    female = ['妈妈', '奶奶', '外婆', '舅妈', '妹妹', '姐姐', '姨妈', '姑姑']
    family_base = {
        "male": {

        },
        "female": {

        }
    }
    friend_base = {
        "male": {

        },
        "female": {

        }
    }
    work_base = {
        "male": {

        },
        "female": {

        }
    }

    def __init__(self, gender):
        pass
