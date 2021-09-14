from common.relations.relation import Relation
from common.yi_base import Yi
from xinpai.gan_zhi_wang_ruo.relation_type import XinPaiRelationType
from common.positions.ming_ju_positions import MingJuPosition


class XinPaiGanZhi:
    def __init__(self, gan_zhi: Yi, position: XinPaiEffectGanZhiPosition):
        pass


class XinPaiRelation:
    def __init__(self, target_gan_zhi: XinPaiGanZhi, effect_gan_zhi: XinPaiGanZhi):
        pass


class XinPaiGanZhiRelation(Relation):
    def __init__(self, target_gan_zhi: Yi, effect_gan_zhi: Yi):
        pass


class XinPaiZhuRelation(XinPaiRelation):
    pass


class WangRuo(XinPaiRelation):
    """
    判断干支旺弱的基础程序
    """

    def __init__(self,
                 target_gan_zhi: Yi,
                 target_gan_zhi_position: XinPaiEffectGanZhiPosition,
                 effect_gan_zhi: Yi,
                 effect_gan_zhi_position: XinPaiEffectGanZhiPosition,
                 target_gan_zhi_kong_wang=False,
                 effect_gan_zhi_kong_wang=False):
        pass
