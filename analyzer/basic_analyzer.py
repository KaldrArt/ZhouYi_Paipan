from common import *
from paipan import *


class BasicAnalyzer:
    def __init__(self, date_str, gender):
        self.pai_pan = PaiPan(date_str, gender=gender)
        PaiPanPrinter(pai_pan=self.pai_pan)
        liu_qin_relation = LiuQinRelation(pai_pan=self.pai_pan)
