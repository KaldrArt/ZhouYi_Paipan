from .dizhi import DiZhi, di_zhi_list
from .tiangan import TianGan, tian_gan_list
from .zhangsheng import zhang_sheng_list, tian_gan_zhang_sheng
from common.relations import TianGanRelation, DiZhiRelation, TianGanDiZhiRelation
from .jiazi import JiaZi, JiaZiBase, jia_zi_list

for tian_gan in tian_gan_list:
    for char in TianGan[tian_gan].value.relations:
        if char in tian_gan_list:
            relation = TianGanRelation(TianGan[tian_gan], TianGan[char])
            TianGan[tian_gan].value.relations[char] = relation.relations['without_yin_yang']
            TianGan[tian_gan].value.relations_with_yin_yang[char] = relation.relations['with_yin_yang']
        else:
            relation = TianGanDiZhiRelation(TianGan[tian_gan], DiZhi[char])
            TianGan[tian_gan].value.relations[char] = relation.relations['without_yin_yang']
            TianGan[tian_gan].value.relations_with_yin_yang[char] = relation.relations['with_yin_yang']

for di_zhi in di_zhi_list:
    for char in DiZhi[di_zhi].value.relations:
        if char in di_zhi_list:
            relation = DiZhiRelation(DiZhi[di_zhi], DiZhi[char])
            DiZhi[di_zhi].value.relations[char] = relation.relations['without_yin_yang']
            DiZhi[di_zhi].value.relations_with_yin_yang[char] = relation.relations['with_yin_yang']
