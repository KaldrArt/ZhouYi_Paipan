from datetime import datetime
from liuyao.common.gua import Gua, LiuYaoGua
from common.jiazi import JiaZi, JiaZiBase
from common.calendar import Solar2LunarCalendar
from common.utils import init_date
from liuyao.common.basic import get_liu_shen_by_ri_gan
from liuyao.common.dazongyi_to_md import DaZongYiTransformer


def __check_code__(code):
    error = False
    code_str = str(code)
    dong_str = code_str[2:]
    if code < 11 or "9" in code_str or "0" in code_str:
        error = True
    elif len(code_str) > 2:
        if "7" in dong_str or "8" in dong_str or '9' in dong_str:
            error = True
    if error:
        raise Exception("卦码错误")
    result = []
    for char in code_str[2:]:
        if char not in result:
            result.append(char)
    result.sort()
    return code_str[0:2] + "".join(result)


class PaiPan:
    def __init__(self, code, yue="", ri="", info={}, print_yin_yang=False):
        self.code = __check_code__(code)
        self.gua_code = self.code[0:2]
        self.info = info
        self.time = info['起卦时间']
        if not yue or not ri:
            self.date, self.solar_to_lunar_date, _ = init_date(self.time)
            self.nian, self.yue, self.ri, self.yinli = Solar2LunarCalendar(self.solar_to_lunar_date)
        else:
            self.nian = ""
            self.yue = yue
            self.ri = ri
        self.ri_zhu: JiaZiBase = JiaZi[self.ri].value
        self.kong_wang = self.ri_zhu.kong_wang
        self.ben_gua = LiuYaoGua(
            int(self.gua_code[0]),
            int(self.gua_code[1]),
            print_yin_yang
        )

        self.dong_code = self.code[2:]
        if len(self.dong_code):
            self.jing_gua = False
            self.bian_gua = self.ben_gua.get_bian_gua_from_code(int(self.dong_code))
        else:
            self.jing_gua = True

        if self.check_paipan_info():
            self.get_pai_pan()
        self.ying_index = self.ben_gua.ying_index
        self.shi_index = self.ben_gua.shi_index
        self.shi_name = self.ben_gua.shi
        self.fu_shen_text = self.ben_gua.fu_shen_list
        self.print_yin_yang = print_yin_yang
        self.ben_gua.set_liu_shen(get_liu_shen_by_ri_gan(self.ri[0]))
        self.ping_tai = self.__set_ping_tai()

    def __set_ping_tai(self):
        pass

    def print_md(self):
        DaZongYiTransformer(self.__str__(), print=True)

    def __str__(self):
        bengua_strs = self.ben_gua.__str__().split("\n")
        ben_gua_liuqin = []
        ben_gua_liuqin.extend(self.ben_gua.liu_qin)
        ben_gua_liuqin.reverse()
        s = "求测人年龄:%s 性别:%s 职业:%s\n" % (self.info['年龄'], self.info['性别'], self.info['职业'])
        for key in self.info:
            if key not in ['年龄', '性别', '职业']:
                s += key + ":%s" % self.info[key] + "\n"
        # s += "起卦时间：%s%s\n" % (self.nian, self.time)
        s += "%s月 %s日(%s空) %s卦" % (self.yue, self.ri, "".join(i.name for i in self.kong_wang), self.code)
        s += "\n"
        s += "    " + "《%s》" % self.ben_gua.name + "\t"
        if not self.jing_gua:
            bingua_strs = self.bian_gua.__str__().split("\n")
            bian_gua_liuqin = []
            bian_gua_liuqin.extend(self.bian_gua.liu_qin)
            bian_gua_liuqin.reverse()

            if self.print_yin_yang:
                s += '\t'
            s += "《%s》" % self.bian_gua.name + "\n"
            for i in range(0, 6):
                if self.fu_shen_text[5 - i]:
                    s += self.fu_shen_text[5 - i] + ""
                else:
                    s += "    "
                s += " " + ben_gua_liuqin[i] + bengua_strs[i]
                if str(6 - i) in self.dong_code:
                    if self.ben_gua.yao_wei_yin_yang[5 - i]:
                        dong_symbol = "○ "
                    else:
                        dong_symbol = "× "
                    s += dong_symbol
                else:
                    if self.ben_gua.yao_wei_yin_yang[5 - i]:
                        s += "、"
                    else:
                        s += ".."
                if self.shi_index - 1 == 5 - i:
                    s += "" + self.shi_name
                elif self.ying_index - 1 == 5 - i:
                    s += "应"
                else:
                    s += "   "
                if self.print_yin_yang:
                    s += "    "
                s += "\t"
                if self.print_yin_yang:
                    s += bian_gua_liuqin[i]
                s += bingua_strs[i]
                if self.bian_gua.yao_wei_yin_yang[5 - i]:
                    s += "、 "
                else:
                    s += ".."
                s += "\t" + self.ben_gua.liu_shen[5 - i] + "\n"
            return s
        else:
            s += "\n"
            for i in range(0, 6):
                if self.fu_shen_text[5 - i]:
                    s += self.fu_shen_text[5 - i]
                else:
                    s += "    "
                s += " " + ben_gua_liuqin[i] + bengua_strs[i]
                if str(6 - i) in self.dong_code:
                    if self.ben_gua.yao_wei_yin_yang[5 - i]:
                        dong_symbol = "○ "
                    else:
                        dong_symbol = "× "
                    s += dong_symbol
                else:
                    if self.ben_gua.yao_wei_yin_yang[5 - i]:
                        s += "、"
                    else:
                        s += ".."
                if self.shi_index - 1 == 5 - i:
                    s += "" + self.shi_name
                elif self.ying_index - 1 == 5 - i:
                    s += "应"
                else:
                    s += "  "
                if self.print_yin_yang:
                    s += "    "
                s += "\t" + self.ben_gua.liu_shen[5 - i] + "\n"
            return s

    def check_paipan_info(self):
        pass

    def get_ri_yue_shi_fen(self):
        pass

    def get_basic_info(self):
        pass


class PaiPanFromCoin(PaiPan):
    pass
