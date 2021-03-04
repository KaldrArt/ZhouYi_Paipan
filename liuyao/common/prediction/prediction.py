from ..paipan.paipan import PaiPan


class Prediction(PaiPan):
    def __init__(self, code, yue="", ri="", info={}, print_yin_yang=False):
        super().__init__(code, yue, ri, info, print_yin_yang)
        self.liu_yao_parse()

    def liu_yao_parse(self):
        """
        获取六个爻位的状态等信息
        :return:
        """
        pass
