from liuyao.common.gua import SanYaoGua, LiuYaoGua
from liuyao.common.basic import get_gua_code_from_gua_name


class Pan:
    di_pan = [
        SanYaoGua.巽, SanYaoGua.离, SanYaoGua.坤,
        SanYaoGua.震, None, SanYaoGua.兑,
        SanYaoGua.艮, SanYaoGua.坎, SanYaoGua.乾
    ]

    def __init__(self, gong_wei_list=[]):
        if len(gong_wei_list) != 9:
            gong_wei_list = self.di_pan
        self.gong_wei_list = gong_wei_list
        self.xun = gong_wei_list[0]
        self.li = gong_wei_list[1]
        self.kun = gong_wei_list[2]
        self.zhen = gong_wei_list[3]
        self.zhong_gong = gong_wei_list[4]
        self.dui = gong_wei_list[5]
        self.gen = gong_wei_list[6]
        self.kan = gong_wei_list[7]
        self.qian = gong_wei_list[8]

    def to_md(self):
        pass

    def to_image(self):
        pass

    def __str__(self):
        result = "小成图：\n\n "
        for i in range(3):
            for line_idx in range(3):
                for j in range(i * 3, i * 3 + 3):
                    gua = self.gong_wei_list[j]
                    if gua:
                        result += gua.value.__str__().split("\n")[line_idx]
                    else:
                        result += " " * 5
                    if j % 3 < 2:
                        result += " │ "
                result += "\n"
                if line_idx % 3 < 2:
                    result += " "
            if i % 3 < 2:
                result += ("─" * 7 + "┼") * 2 + "─" * 7 + "\n "
        return result


class XiaoChengTu:
    di_pan = Pan()

    def __init__(self, ben_gua: LiuYaoGua, bian_gua: LiuYaoGua):
        self.ben_gua = ben_gua
        self.bian_gua = bian_gua
        self.zhong_gong = self.__get_zhong_gong()
        self.tian_pan = self.__get_tian_pan()

    def __get_zhong_gong(self):
        return None

    def __get_tian_pan(self):
        tian_pan_list = [
            self.ben_gua.shang_hu_gua, SanYaoGua[self.ben_gua.waigua.name], self.ben_gua.xia_hu_gua,
            SanYaoGua[self.bian_gua.waigua.name], self.zhong_gong, SanYaoGua[self.bian_gua.neigua.name],
            self.bian_gua.shang_hu_gua, SanYaoGua[self.ben_gua.neigua.name], self.bian_gua.xia_hu_gua
        ]
        return Pan(tian_pan_list)

    def __get_gui_cang(self):
        pass

    def __get_zhong_gong_relation(self):
        pass

    def __get_gong_wei_ji_xiong(self):
        pass

    def __get_pang_tui(self):
        pass

    def __get_zheng_tui(self):
        pass

    def print_di_pan(self):
        print("\n地盘" + self.di_pan.__str__())

    def print_tian_pan(self):
        print("\n天盘" + self.tian_pan.__str__())


def get_xiao_cheng_tu_from_4_codes(ben_gua_shang: int,
                                   ben_gua_xia: int,
                                   bian_gua_shang: int,
                                   bian_gua_xia: int) -> XiaoChengTu:
    ben_gua = LiuYaoGua(ben_gua_shang, ben_gua_xia)
    bian_gua = LiuYaoGua(bian_gua_shang, bian_gua_xia)
    return XiaoChengTu(ben_gua, bian_gua)


def get_xiao_cheng_tu_from_gua_code(ben_gua_code: int, bian_gua_code: int) -> XiaoChengTu:
    return get_xiao_cheng_tu_from_4_codes(
        ben_gua_shang=ben_gua_code // 10,
        ben_gua_xia=ben_gua_code % 10,
        bian_gua_shang=bian_gua_code // 10,
        bian_gua_xia=bian_gua_code % 10
    )


def get_xiao_cheng_tu_from_gua_name(ben_gua_name, bian_gua_name) -> XiaoChengTu:
    ben_gua_code = get_gua_code_from_gua_name(ben_gua_name)
    bian_gua_code = get_gua_code_from_gua_name(bian_gua_name)
    return get_xiao_cheng_tu_from_gua_code(ben_gua_code, bian_gua_code)

# get_xiao_cheng_tu_from_gua_name("大蓄", '中孚').print_tian_pan()

# get_xiao_cheng_tu_from_gua_code(15, 25).print_tian_pan()
