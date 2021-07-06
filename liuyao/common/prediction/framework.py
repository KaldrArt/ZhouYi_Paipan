from common.prediction.stage import Stage


class Framework(Stage):
    """
    根据权和平台，定平台爻位的态、平台之间的作用关系（例如三合、三会）。
    根据态，定平台爻位和静爻的力量。
    从而得到每一个爻位的旺衰。
    """

    def __init__(self, paipan):
        self.ri
        self.yue
        self.platforms = self.get_platforms()

        self.platform_relations()

    def get_platforms(self):
        """
        获取平台
        """
        pass

    def platform_relations(self):
        """
        判断平台之间的关系
        """
        pass
