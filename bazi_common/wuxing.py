from enum import Enum

wu_xing_list = list("木火土金水")


class WuXingBase:
    def __init__(self, name):
        if name not in wu_xing_list:
            raise Exception("%s不是有效的五行" % name)
        self.name = name
        self.index = wu_xing_list.index(name)


class WuXing(Enum):
    木 = WuXingBase('木')
    火 = WuXingBase('火')
    土 = WuXingBase('土')
    金 = WuXingBase('金')
    水 = WuXingBase('水')
