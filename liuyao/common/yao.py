class Yao:
    def __init__(self,
                 position,  # 爻位
                 tiangan,
                 dizhi,
                 liuqin,
                 liushen,
                 gua,
                 gong,
                 shi=False,
                 ying=False,
                 fushen=None,
                 feishen=None):
        self.position = position
        self.tiangan = tiangan
        self.dizhi = dizhi
        self.liuqin = liuqin
        self.liushen = liushen
        self.gua = gua
        self.gong = gong
        self.shi = shi
        self.ying = ying
        if shi or ying:
            self.shi = gong.name
        self.fushen = fushen
        self.feishen = feishen


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
