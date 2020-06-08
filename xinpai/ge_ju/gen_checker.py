from paipan.pai_pan import PaiPan
from ..mu_ku_lun import MuKuLun


class GenChecker:
    """
    检查一个天干是否有根
    """

    def __init__(self, pai_pan: PaiPan):
        self.pai_pan = pai_pan
        self.yue_gan = False
        self.shi_gan = False

    def check_yue_gan(self):
        pass

    def check_shi_gan(self):
        pass
