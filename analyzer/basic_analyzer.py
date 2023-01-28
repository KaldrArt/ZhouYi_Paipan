from bazi_common import *
from paipan import *


class BasicAnalyzer:
    def __init__(self, date_str, gender=True):
        self.pai_pan = PaiPan(date_str, gender=gender)
        PaiPanPrinter(pai_pan=self.pai_pan, print_liu_nian_year=True)
        self.liu_qin_relation = LiuQinBasic(pai_pan=self.pai_pan)
        print(self.liu_qin_relation)
