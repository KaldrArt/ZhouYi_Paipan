from bazi_common.dizhi import DiZhi


class Yao:
    def __init__(self,
                 position,  # 爻位
                 dizhi,
                 liuqin,
                 liushen,
                 gua,
                 gong,
                 liuyaogua=False,
                 shi=False,
                 ying=False,
                 fushen=None,
                 feishen=None,
                 tiangan=None):
        self.position = position
        self.tiangan = tiangan
        self.dizhi = dizhi
        self.liuqin = liuqin
        self.liushen = liushen
        self.gua = gua
        self.gong = gong
        self.shi = shi
        self.ying = ying
        # if shi or ying:
        #  self.shi = gong
        self.liuyaogua = liuyaogua
        self.fushen = fushen
        self.feishen = feishen
        self.fu_yao = self.set_fushen()

    def set_fushen(self):
        if self.fushen:
            return FuYao(self.position,
                         DiZhi[self.fushen[1]],
                         self.fushen[0],
                         self.liushen,
                         self.gua,
                         self.gong,
                         self.liuyaogua,
                         self.shi,
                         self.ying,
                         feishen=self,
                         tiangan=self.tiangan
                         )
        else:
            return None

    def __str__(self):
        text = "%s %s%s 世%s 应%s %s" % (
            self.fushen,
            self.liuqin,
            self.dizhi,
            self.shi,
            self.ying,
            self.liushen
        )
        return text


class JingYao(Yao):
    pass


class FuYao(JingYao):
    pass


class DongYao(JingYao):
    pass


class BianYao(DongYao):
    pass


class YanYao(BianYao):
    pass


class ChuFuYao(DongYao):
    pass


class ShiYao(Yao):
    pass


class YingYao(Yao):
    pass
