from analyzer.basic_analyzer import BasicAnalyzer
from .ge_ju.ge_ju import GeJu


class XinPaiAnalyzer(BasicAnalyzer):
    def __init__(self, date_str, gender, ge_ju: GeJu):
        super().__init__(date_str, gender)
        if ge_ju:
            pass
        else:
            pass
   
