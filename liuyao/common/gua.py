from enum import Enum
from liuyao.common.basic import gua_wu_xing_list, gua_liu_qin, gua_list, \
    gua_dizhi_map, gua_yao_list, get_gua_name_from_code, gua_dizhi_list, \
    get_liu_shen_by_ri_gan, get_liu_qin_of_target, get_gua_from_yao_wei
from liuyao.common.dizhi import DiZhi
from liuyao.common.yao import Yao, DongYao, BianYao, JingYao
from liuyao.common.prediction.platform import Platform


def __check_dong_code__(code):
    if not code:
        raise Exception("三爻卦的动爻不能为空")
    code_str = str(code)
    c = ""
    if len(code_str) > 3:
        raise Exception("三爻卦的动爻数量最大为3")
    else:
        for char in code_str:
            i = int(char)
            if i > 3:
                i = i - 3
            if i < 1 or i > 3:
                raise Exception("三爻卦的动爻必须是1、2、3")
            if char in c:
                raise Exception("三爻卦的动爻不要重复")
            c += str(i)
    return c


def get_gua_name_from_yao(yao_list):
    for j in range(0, 8):
        item = gua_yao_list[j]
        bingo = True
        for i in [0, 1, 2]:
            if yao_list[i] != item[i]:
                bingo = False
                break
        if bingo:
            return gua_list[j]
    raise Exception("不是有效的爻位，例如兑卦为[0,1,1]")


class Gua:
    def __init__(self, name, yin_yang=False, up=True, ename=""):
        self.name = name
        self.ename = ename
        self.yin_yang = yin_yang
        self.up = up
        self.index = gua_list.find(name) + 1
        self.dizhi = gua_dizhi_map[self.name]
        self.yao_wei = gua_yao_list[self.index - 1]
        self.wu_xing = gua_wu_xing_list[self.index - 1]

    def get_bian_gua(self, dong_code=1):
        dong_c = __check_dong_code__(dong_code)
        bian_gua_yao_wei = []
        bian_gua_yao_wei.extend(self.yao_wei)
        for c in dong_c:
            bit = int(c) - 1
            bian_gua_yao_wei[bit] = 1 if bian_gua_yao_wei[bit] == 0 else 0
        return Gua(get_gua_name_from_yao(bian_gua_yao_wei))

    def __str__(self):
        s = ""
        for i in range(2, -1, -1):
            if self.yao_wei[i] == 1:
                s += " ■■■ "
            else:
                s += " ■ ■ "
            s += "\n"
        return s


class SanYaoGua(Enum):
    乾 = Gua("乾", True, True, 'qian')
    兑 = Gua("兑", False, False, 'dui')
    离 = Gua("离", False, True, 'li')
    震 = Gua("震", True, True, 'zhen')
    巽 = Gua("巽", False, False, 'xun')
    坎 = Gua("坎", True, False, 'kan')
    艮 = Gua("艮", True, True, 'gen')
    坤 = Gua("坤", False, False, 'kun')


def get_gua_from_code(code) -> Gua:
    code = code % 8
    return SanYaoGua[gua_list[code - 1]].value


class LiuYaoGua:
    def __init__(self,
                 waigua_code=1,
                 neigua_code=1,
                 ri_gan='甲',
                 dong_code="",
                 print_with_yin_yang=False):
        self.print_with_yin_yang = print_with_yin_yang
        self.dong_code = [int(s) for s in dong_code]
        self.name, self.gong, self.gong_wei = get_gua_name_from_code(
            waigua_code * 10 + neigua_code)
        self.ri_gan = ri_gan
        self.neigua_code = neigua_code % 8
        self.waigua_code = waigua_code % 8
        if self.waigua_code == 0:
            self.waigua_code = 8
        self.neigua: Gua = get_gua_from_code(self.neigua_code)
        self.waigua: Gua = get_gua_from_code(self.waigua_code)
        self.yao_wei_yin_yang = self.__get_yao_wei()
        self.dizhi = self.__get_dizhi()
        self.liu_chong = self.__get_liu_chong()
        self.liu_he = self.__get_liu_he()
        self.is_you_hun = self.__get_you_hun()
        self.is_gui_hun = self.__get_gui_hun()
        self.shi, self.shi_index, self.ying_index = self.__set_shi_ying()
        self.wu_xing = gua_wu_xing_list[gua_list.find(self.shi)]
        self.liu_qin, self.fu_shen, self.fu_shen_list = self.__set_liu_qin()
        self.liu_shen = self.__set_liushen__()
        if dong_code:
            self.bian_gua = self.get_bian_gua_from_code(dong_code)
            self.bian_gua_liuqin = self.__set_biangua_liuqin()
            self.yao_and_platforms = self.__set_yaos_and_platforms__()
        else:
            self.bian_gua = None
        self.shang_hu_gua = self.__set_shang_hu_gua()
        self.xia_hu_gua = self.__set_xia_hu_gua()
        self.de_pei = self.__set_de_pei()
        self.direction = self.__set_direction()
        self.ji_xiong_hui_lin = self.__set_jixionghuilin()

    def __set_jixionghuilin(self):
        if self.direction == '往':
            if self.de_pei:
                result = '亨'
            else:
                result = "悔"
        elif self.direction == '来':
            if self.de_pei:
                result = "贞"
            else:
                result = "吝"
        elif self.direction == '阖':
            if self.de_pei:
                result = '吉'
            else:
                result = "凶"
        else:
            if self.de_pei:
                result = "害"
            else:
                result = '利'
        return result

    def __set_direction(self):
        if self.neigua.up and self.waigua.up:
            result = "往"
        elif self.neigua.up and not self.waigua.up:
            result = "阖"
        elif not self.neigua.up and self.waigua.up:
            result = '辞'
        else:
            result = '来'
        return result

    def __set_de_pei(self):
        if self.waigua.yin_yang and not self.neigua.yin_yang:
            return True
        elif self.neigua.yin_yang and not self.waigua.yin_yang:
            return True
        return False

    def __set_shang_hu_gua(self):
        first_yao = self.neigua.yao_wei[-1]
        second_yao = self.waigua.yao_wei[0]
        third_yao = self.waigua.yao_wei[1]
        return SanYaoGua[get_gua_from_yao_wei([first_yao, second_yao, third_yao])]

    def __set_xia_hu_gua(self):
        first_yao = self.neigua.yao_wei[1]
        second_yao = self.neigua.yao_wei[2]
        third_yao = self.waigua.yao_wei[0]
        return SanYaoGua[get_gua_from_yao_wei([first_yao, second_yao, third_yao])]

    def __set_biangua_liuqin(self):
        result = []
        target_dizhi = self.neigua.dizhi['inside'][0]
        target_dizhi_liuqin = self.liu_qin[0]
        for effect_dizhi in self.bian_gua.dizhi:
            liu_qin = get_liu_qin_of_target(
                target_dizhi.value.name,
                target_dizhi_liuqin,
                effect_dizhi.value.name)
            result.append(liu_qin)
        # print(result)
        return result

    def __set_liushen__(self):
        return get_liu_shen_by_ri_gan(self.ri_gan)

    def __set_yaos_and_platforms__(self):
        yaos = [False, False, False, False, False, False]
        ben_gua_yaos = [False, False, False, False, False, False]
        bian_gua_yaos = [False, False, False, False, False, False]
        platforms = [False, False, False, False, False, False]
        for i in range(5, -1, -1):
            if i < 3:
                gua = self.neigua
                bian_gua = self.bian_gua.neigua
            else:
                gua = self.waigua
                bian_gua = self.bian_gua.waigua
            if i + 1 in self.dong_code:
                bengua_yao = self.__set_dongyao__(i, gua)
                biangua_yao = self.__set_bianyao__(i, bian_gua)
            else:
                bengua_yao = self.__set_jingyao__(i, gua)
                biangua_yao = self.__set_yao__(i, bian_gua)
            ben_gua_yaos[i] = bengua_yao
            bian_gua_yaos[i] = biangua_yao
            yaos[i] = (bengua_yao, biangua_yao)
            if i + 1 in self.dong_code:
                platform = self.__set_platform__(i, bengua_yao, biangua_yao)
                platforms[i] = platform

        return {
            "yaos": {
                "ben_gua": ben_gua_yaos,
                "bian_gua": bian_gua_yaos,
                "list": yaos
            },
            "platforms": platforms
        }

    def __set_dongyao__(self, yao_index, gua):
        return self.__set_yao__(yao_index, gua, DongYao)

    def __set_jingyao__(self, yao_index, gua):
        return self.__set_yao__(yao_index, gua, JingYao)

    def __set_yao__(self, yao_index, gua, yao_class=Yao):
        i = yao_index
        if i < 3:
            dizhi = gua.dizhi['inside'][i]
        else:
            dizhi = gua.dizhi['outside'][i - 3]
        if yao_class.__name__ in ['Yao', 'BianYao']:
            liuqin = self.bian_gua_liuqin[i]
        else:
            liuqin = self.liu_qin[i]
        yao = yao_class(i + 1,
                        dizhi,
                        liuqin,
                        self.liu_shen[i],
                        gua,
                        self.shi,
                        self,
                        True if i + 1 == self.shi_index else False,
                        True if i + 1 == self.ying_index else False,
                        self.fu_shen_list[i]
                        )

        return yao

    def __set_bianyao__(self, yao_index, gua):
        return self.__set_yao__(yao_index, gua, BianYao)

    def __set_platform__(self, index, dongyao, bianyao):
        return Platform(dongyao,
                        bianyao,
                        index,
                        self,
                        self.bian_gua)

    def __set_shi_ying(self):
        shi = self.gong
        shi_index = self.gong_wei
        if self.gong_wei == 0:
            shi_index = 6
        elif self.gong_wei == 6:
            shi_index = 4
        elif self.gong_wei == 7:
            shi_index = 3
        ying_index = (shi_index + 3) % 6
        if ying_index == 0:
            ying_index = 6
        return shi, shi_index, ying_index

    def __set_liu_qin(self):
        liu_qin = [i.value.get_liu_qin_to_wu_xing(
            self.wu_xing) for i in self.dizhi]
        absenced_liu_qin = []
        gong_index = gua_list.find(self.gong)
        fu_gua_liu_qin = gua_liu_qin[gong_index]
        fu_gua_di_zhi = "".join(gua_dizhi_list[gong_index])
        for i in range(0, 6):
            lq = fu_gua_liu_qin[i]
            if lq not in liu_qin:
                absenced_liu_qin.append((lq, fu_gua_di_zhi[5 - i], 5 - i))
        fu_shen_list = [False, False, False, False, False, False]
        for i in absenced_liu_qin:
            fu_shen_list[i[2]] = i[0] + i[1]
        fu_shen = [DiZhi[i[1]] if i else False for i in fu_shen_list]
        return liu_qin, fu_shen, fu_shen_list

    def set_liu_shen(self, liu_shen):
        self.liu_shen = liu_shen

    def __str__(self):
        s = ""
        for i in range(5, -1, -1):
            s += self.dizhi[i].value.name
            if self.print_with_yin_yang:
                if self.yao_wei_yin_yang[i] == 1:
                    s += " ■■■ "
                else:
                    s += " ■ ■ "
            s += "\n"
        return s

    def get_bian_gua_from_code(self, code):
        code_str = str(code)
        unique_code_str = ""
        xiagua_code = ""
        shanggua_code = ""
        for c in code_str:
            if int(c) > 6 or int(c) < 0:
                raise Exception("变爻只能是1到6的一个数字")
            if c not in unique_code_str:
                unique_code_str += c
        for c in unique_code_str:
            if int(c) < 4:
                xiagua_code += c
            else:
                shanggua_code += "%s" % (int(c) - 3)
        if xiagua_code:
            xiagua_bian = int(self.neigua.get_bian_gua(int(xiagua_code)).index)
        else:
            xiagua_bian = self.neigua.index
        if shanggua_code:
            shanggua_bian = int(
                self.waigua.get_bian_gua(int(shanggua_code)).index)
        else:
            shanggua_bian = self.waigua.index
        return LiuYaoGua(shanggua_bian,
                         xiagua_bian,
                         self.ri_gan,
                         print_with_yin_yang=self.print_with_yin_yang)

    def __get_dizhi(self):
        result = []
        result.extend(self.neigua.dizhi['inside'])
        result.extend(self.waigua.dizhi['outside'])
        return result

    def __get_yao_wei(self):
        result = []
        result.extend(self.neigua.yao_wei)
        result.extend(self.waigua.yao_wei)
        return result

    def __get_you_hun(self):
        if self.gong_wei == 6:
            return True
        else:
            return False

    def __get_gui_hun(self):
        if self.gong_wei == 7:
            return True
        else:
            return False

    def __get_liu_chong(self):
        if self.neigua_code == self.waigua_code:
            return True
        elif self.neigua_code == 1 and self.waigua_code == 4:
            return True
        elif self.neigua_code == 4 and self.waigua_code == 1:
            return True
        else:
            return False

    def __get_liu_he(self):
        liu_he_list = [
            [6, 2], [7, 3], [1, 8], [4, 7]
        ]
        for item in liu_he_list:
            if (self.neigua_code == item[0]
                and self.waigua_code == item[1]) \
                    or (self.neigua_code == item[1]
                        and self.waigua_code == item[0]):
                return True
        return False
