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

    def gua_framework(self):
        """
        分析一个卦的架构
        架构是指卦的日月、平台和静爻。
        日月对任何一个平台、静爻的能量，取决于平台。
        平台对静爻的能量，取决于日月和其他平台的作用规律。
        搞清楚架构，就知道了各个位置的能量释放，因此就能够知道各个爻位的状态。
        """
        pass

    
