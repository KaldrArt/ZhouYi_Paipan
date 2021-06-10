from liuyao.common.gua import LiuYaoGua


class Platform:
    def __init__(self, position: int, ben_gua: LiuYaoGua, bian_gua: LiuYaoGua):
        self.position = position
        self.ben_gua = ben_gua
        self.bian_gua = bian_gua

    def __str__(self):
        result = self.ben_gua
        if self.ben_gua.fu_shen_list[position]:
            print(self.ben_gua.fu_shen_list[position])
