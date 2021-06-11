# 卦装地支
from liuyao.common.dizhi import DiZhi, di_zhi_list

gua_list = "乾兑离震巽坎艮坤"
gua_wu_xing_list = "金金火木木水土土"
gua_yao_list = [
    [1, 1, 1],
    [1, 1, 0],
    [1, 0, 1],
    [1, 0, 0],
    [0, 1, 1],
    [0, 1, 0],
    [0, 0, 1],
    [0, 0, 0]
]
gua_name = [
    ['乾为天', '天风姤', '天山遁', '天地否', '风地观', '山地剥', '火地晋', '大有'],
    ['兑为泽', '泽水困', '泽地萃', '泽山咸', '水山蹇', '地山谦', '小过', '归妹'],
    ['离为火', '火山旅', '火风鼎', '未济', '山水蒙', '风水涣', '天水讼', '同人'],
    ['震为雷', '雷地豫', '雷水解', '雷风恒', '地风升', '水风井', '大过', '泽雷随'],
    ['巽为风', '小蓄', '家人', '风雷益', '无妄', '噬嗑', '山雷颐', '山风蛊'],
    ['坎为水', '水泽节', '水雷屯', '既济', '泽火革', '雷火丰', '明夷', '地水师'],
    ['艮为山', '山火贲', '大蓄', '山泽损', '火泽睽', '天泽履', '中孚', '风山渐'],
    ['坤为地', '地雷复', '地泽临', '地天泰', '大壮', '泽天夬', '水天需', '水地比']
]
gua_gong = [
    [11, 15, 17, 18, 58, 78, 38, 31],
    [22, 26, 28, 27, 67, 87, 47, 42],
    [33, 37, 35, 36, 76, 56, 16, 13],
    [44, 48, 46, 45, 85, 65, 25, 24],
    [55, 51, 53, 54, 14, 34, 74, 75],
    [66, 62, 64, 63, 23, 43, 83, 86],
    [77, 73, 71, 72, 32, 12, 52, 57],
    [88, 84, 82, 81, 41, 21, 61, 68]
]

liu_shen = "龙雀勾蛇虎玄"
liu_shen_tian_gan_list = [1, 1, 2, 2, 3, 4, 5, 5, 6, 6]
tian_gan = "甲乙丙丁戊己庚辛壬癸"


def get_liu_shen_by_ri_gan(ri_gan):
    first_liu_shen = liu_shen_tian_gan_list[tian_gan.find(ri_gan)] - 1
    result = []
    for i in range(0, 6):
        index = (first_liu_shen + i) % 6
        result.append(liu_shen[index])
    return result


def get_gua_name_from_code(code):
    for j in range(0, 8):
        for i in range(0, 8):
            if code == gua_gong[j][i]:
                return gua_name[j][i], gua_list[j], i
    return "", "", -1


gua_liu_qin = [
    '父兄官父财孙',
    '父兄孙父财官',
    '兄孙财官孙父',
    '财官孙财兄父',
    '兄孙财官父财',
    '兄官父财官孙',
    '官财兄孙父兄',
    '孙财兄官父兄'
]

gua_dizhi_map = {}

gua_dizhi_list = [
    ['子寅辰', '午申戌'],
    ['巳卯丑', '亥酉未'],
    ['卯丑亥', '酉未巳'],
    ["子寅辰", '午申戌'],
    ['丑亥酉', '未巳卯'],
    ['寅辰午', '申戌子'],
    ["辰午申", '戌子寅'],
    ['未巳卯', '丑亥酉']
]


def generate_gua_dizhi_map():
    for idx in range(len(gua_list)):
        gua_dizhi_map[gua_list[idx]] = {
            "inside": [DiZhi[dz] for dz in gua_dizhi_list[idx][0]],
            "outside": [DiZhi[dz] for dz in gua_dizhi_list[idx][1]],
        }


generate_gua_dizhi_map()

liu_qin = "兄孙财官父"
wu_xing = "水木火土金"


def get_liu_qin_of_target(
        target_dizhi: str,
        target_dizhi_liuqin: str,
        effect_dizhi: str):
    if effect_dizhi not in di_zhi_list or \
            target_dizhi not in di_zhi_list or \
            target_dizhi_liuqin not in liu_qin:
        raise Exception('输入参数错误 %s,%s,%s' % (
            target_dizhi,
            target_dizhi_liuqin,
            effect_dizhi))
    target_dizhi_liuqin_index = liu_qin.index(target_dizhi_liuqin)
    target_wuxing_index = wu_xing.index(DiZhi[target_dizhi].value.wu_xing.name)
    effect_wuxing_index = wu_xing.index(DiZhi[effect_dizhi].value.wu_xing.name)
    effect_liuqin_index = target_dizhi_liuqin_index+(effect_wuxing_index
                                                     - target_wuxing_index)
    return liu_qin[effect_liuqin_index % 5]
