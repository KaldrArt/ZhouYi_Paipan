from common.relations import *
from common import *

for char in di_zhi_list:
    for c in di_zhi_list:
        r = DiZhiRelation(DiZhi[char], DiZhi[c])
        print(r.name, r.relation_names, r.relation_names_with_yin_yang)

for char in tian_gan_list:
    for c in tian_gan_list:
        r = TianGanRelation(TianGan[char], TianGan[c])
        print(r.name, r.relation_names, r.relation_names_with_yin_yang)

for char in tian_gan_list:
    for c in di_zhi_list:
        r = TianGanDiZhiRelation(TianGan[char], DiZhi[c])
        print(r.name, r.relation_names, r.relation_names_with_yin_yang)

for c in di_zhi_list:
    for char in tian_gan_list:
        r = TianGanDiZhiRelation(TianGan[char], DiZhi[c])
        print(r.name, r.relation_names, r.relation_names_with_yin_yang)
