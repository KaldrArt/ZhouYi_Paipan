from liuyao.common.gua import SanYaoGua, LiuYaoGua


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

    def print_di_pan(self):
        print("\n地盘" + self.di_pan.__str__())

    def print_tian_pan(self):
        print("\n天盘" + self.tian_pan.__str__())
