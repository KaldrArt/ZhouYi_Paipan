from liuyao.common.paipan.paipan import PaiPan

paipan = PaiPan(231, save=False)
print(paipan.ben_gua.gong)
print(paipan.ben_gua.gong_wei)
print(paipan.ben_gua.liu_shen)
print(paipan.ben_gua.liu_qin)
print(paipan.ben_gua.fu_shen)
print(paipan.ben_gua.fu_shen_list)
print(paipan.ben_gua.shi)
print(paipan.ben_gua.shi_index)
print(paipan.ben_gua.ying_index)
print(paipan)
for yao in paipan.ben_gua.yao_and_platforms['yaos']['ben_gua']:
    print(yao)
print()
for yao in paipan.ben_gua.yao_and_platforms['yaos']['bian_gua']:
    print(yao)
print()
for yao in paipan.ben_gua.yao_and_platforms['yaos']['list']:
    print(yao[0], "|", yao[1])

for platform in paipan.ben_gua.yao_and_platforms['platforms']:
    print(platform)
