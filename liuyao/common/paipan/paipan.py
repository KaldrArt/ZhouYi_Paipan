from liuyao.common.gua import LiuYaoGua
from common.jiazi import JiaZi, JiaZiBase
from common.calendar import Solar2LunarCalendar
from common.utils import init_date
from liuyao.common.basic import get_liu_shen_by_ri_gan
from liuyao.common.paipan_parser.dazongyi_to_md import DaZongYiTransformer
from liuyao.common.zh_dict.stroke import get_stroke
from datetime import datetime
import math


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
    def __init__(self, code, yue="", ri="", info={"年龄": 34, "性别": "男", "职业": "IT", "起卦时间": ""}, print_yin_yang=False):
        self.code = __check_code__(code)
        self.gua_code = self.code[0:2]
        self.info = info
        self.time = info['起卦时间']
        if not self.time:
            self.time = datetime.now().strftime("%Y/%m/%dT%H:%M:%S")
            info['起卦时间'] = datetime.now().strftime("%Y年%m月%d日%H:%M:%S")
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


class PaiPanFromSentence(PaiPan):
    def __init__(self, chars="", yue="", ri="", shi="", info={"年龄": 34, "性别": "男", "职业": "IT", "起卦时间": ""},
                 print_yin_yang=False):
        self.chars = chars
        if not shi:
            self.shi = "子丑寅卯辰巳午未申酉戌亥".index("子丑寅卯辰巳午未申酉戌亥子"[math.ceil(datetime.now().hour / 2)]) + 1
        else:
            self.shi = "子丑寅卯辰巳午未申酉戌亥".index(shi) + 1
        self.strokes = self.get_stroke(chars)
        code = self.get_code(self.strokes, self.shi)
        super(PaiPanFromSentence, self).__init__(code, yue, ri, info=info, print_yin_yang=print_yin_yang)

    def get_code(self, strokes, shi):
        char_count = len(strokes)
        shang_gua = sum(strokes[0:char_count // 2]) % 8
        if shang_gua == 0:
            shang_gua = 8
        xia_gua = sum(strokes[char_count // 2:]) % 8
        if xia_gua == 0:
            xia_gua = 8
        dong_yao = (sum(strokes) + shi) % 6
        if dong_yao == 0:
            dong_yao = 6
        return shang_gua * 100 + xia_gua * 10 + dong_yao

    def get_stroke(self, chars):
        stroke_count_and_alphabet_index = []
        alphabets = "abcdefghijklmnopqrstuvwxyz"
        nums = "0123456789"
        alphabets += alphabets.upper()
        for char in chars:
            if char in alphabets:
                stroke_count_and_alphabet_index.append(alphabets.index(char))
            elif char in nums:
                stroke_count_and_alphabet_index.append(nums.index(char))
            else:
                n = get_stroke(char)  # 括号等没有笔画
                if n:
                    stroke_count_and_alphabet_index.append(n)
        return stroke_count_and_alphabet_index
