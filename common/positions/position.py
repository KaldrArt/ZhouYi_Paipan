from common.yi_base import YiBase
from common.positions.ming_ju_positions import MingJuPosition, \
    ming_ju_position_list
from common.positions.da_yun_liu_nian_position import DaYunLiuNianPosition, \
    da_yun_liu_nian_position_list


class Position:
    def __init__(self,
                 yi: YiBase,
                 ming_yun_position):
        self.yi = yi
        if isinstance(ming_yun_position, str):
            if ming_yun_position in da_yun_liu_nian_position_list:
                self.position = DaYunLiuNianPosition[ming_yun_position]
            elif ming_yun_position in ming_ju_position_list:
                self.position = MingJuPosition[ming_yun_position]
            else:
                raise "输入的 ming_yun_position 参数必须是位置信息"
        else:
            self.position = ming_yun_position

    def build_effect_score(self):
        pass

    def effect_from(self):
        pass

    def effect_to(self):
        pass
