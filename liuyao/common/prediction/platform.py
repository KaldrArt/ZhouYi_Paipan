from liuyao.common.yao import Yao, DongYao, BianYao, YanYao, FuYao, JingYao
from enum import Enum


class PlatformType(Enum):
    pass


class Platform:
    def __init__(self,
                 ben_gua_yao,
                 bian_gua_yao,
                 position: int,
                 ben_gua,
                 bian_gua):
        self.position = position
        self.ben_gua_yao = ben_gua_yao
        self.bian_gua_yao = bian_gua_yao
        self.ben_gua = ben_gua
        self.bian_gua = bian_gua
        self.fu_shen: FuYao = self.__get_fushen()

    def __get_fushen(self):
        return self.ben_gua_yao.fu_yao

    def set_platform_type(self):
        pass

    def __str__(self):
        result = "%s%s %s%s %s%s %s%s %s" % (
            self.fu_shen.liuqin if self.fu_shen else "  ",
            self.fu_shen.dizhi.name if self.fu_shen else "  ",
            self.ben_gua_yao.liuqin,
            self.ben_gua_yao.dizhi.name,
            self.ben_gua_yao.gong if self.ben_gua_yao.shi else "  ",
            "世" if self.ben_gua_yao.shi else
            "应" if self.ben_gua_yao.ying else "  ",
            self.bian_gua_yao.liuqin,
            self.bian_gua_yao.dizhi.name,
            self.ben_gua_yao.liushen
        )
        return result


class PlatformWithRiYue(Platform):
    pass
