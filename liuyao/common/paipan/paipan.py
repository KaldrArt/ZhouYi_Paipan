from liuyao.common.gua import LiuYaoGua
from liuyao.common.prediction.platform import Platform
from common.jiazi import JiaZi, JiaZiBase
from common.calendar import Solar2LunarCalendar
from common.utils import init_date
# from liuyao.common.basic import get_liu_shen_by_ri_gan
from liuyao.common.paipan_parser.dazongyi_to_md import DaZongYiTransformer
from liuyao.common.zh_dict.stroke import get_stroke
from datetime import datetime, timedelta
import math
import re
from common.prediction.dao import Dao
from liuyao.xiaochengtu.xiaochengtu import XiaoChengTu

default_info = {"年龄": 34, "性别": "男", "职业": "IT", "起卦时间": ""}


def normalize_num_code(input_code):
    result = []
    for i, c in enumerate(str(input_code)):
        ic = int(c)
        m = 6
        if i in [0, 1]:
            m = 8
        mc = ic % m
        if mc == 0:
            mc = m
        result.append(str(mc))
        i += 1

    return "".join(result)


def __check_code__(code):
    error = False
    code_str = str(code)
    dong_str = code_str[2:]
    if int(code) < 11 or "9" in code_str or "0" in code_str:
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


class PaiPan(Dao):
    def __init__(self, code, nian=0, yue=0, ri=0, shi=0,
                 info=default_info, print_yin_yang=False, save=True):
        self.code = __check_code__(code)
        self.gua_code = self.code[0:2]
        self.info = info
        self.time = info['起卦时间']
        self.save = save
        # 日月完整，用日月来代表事项时间
        if ri and yue:
            if not nian:
                nian = datetime.now().year
            base_time = datetime(int(nian), int(yue), int(ri))
            self.time = (base_time + timedelta(hours=shi)
                         ).strftime("%Y/%m/%dT%H:%M:%S")
            if shi:
                if shi == 23:
                    base_time += timedelta(days=1)

            self.nian, self.yue, self.ri, self.yinli = Solar2LunarCalendar(
                base_time.strftime("%Y/%m/%d %H:%M:%S"))
        # 没有完整的日月，也没有设置起卦时间，设置为当前时间
        elif not self.time:
            self.time = datetime.now().strftime("%Y/%m/%dT%H:%M:%S")
            info['起卦时间'] = datetime.now().strftime("%Y/%m/%dT%H:%M:%S")
            self.nian, self.yue, self.ri, self.yinli = Solar2LunarCalendar(
                datetime.now().strftime("%Y/%m/%d"))
        # 没有完整的日月，有起卦时间，用起卦时间来代表事项时间
        else:
            self.date, self.solar_to_lunar_date, _ = init_date(self.time)
            self.nian, self.yue, self.ri, self.yinli = Solar2LunarCalendar(
                self.solar_to_lunar_date)

        self.dong_code = self.code[2:]
        self.ri_zhu: JiaZiBase = JiaZi[self.ri].value
        self.kong_wang = self.ri_zhu.kong_wang
        self.ben_gua = LiuYaoGua(
            int(self.gua_code[0]),
            int(self.gua_code[1]),
            self.ri[0],
            self.dong_code,
            print_yin_yang
        )

        if len(self.dong_code):
            self.jing_gua = False
            self.bian_gua = self.ben_gua.bian_gua
        else:
            self.bian_gua = self.ben_gua
            self.jing_gua = True

        if self.check_paipan_info():
            self.get_pai_pan()
        self.ying_index = self.ben_gua.ying_index
        self.shi_index = self.ben_gua.shi_index
        self.shi_name = self.ben_gua.shi
        self.fu_shen_text = self.ben_gua.fu_shen_list
        self.print_yin_yang = print_yin_yang
        # self.ben_gua.set_liu_shen(get_liu_shen_by_ri_gan(self.ri[0]))
        # self.ping_tai = self.__set_ping_tai()
        self.xiao_cheng_tu = XiaoChengTu(self.ben_gua, self.bian_gua)
        if save:
            self.print_md()

    def __set_ping_tai(self):
        result = []
        for code in self.dong_code:
            platform = Platform(int(code), self.ben_gua, self.bian_gua)
            result.append(platform)
        return result

    def print_md(self, neet_print=False):
        return DaZongYiTransformer(
            self.__str__(),
            print=neet_print, save=self.save)

    def __str__(self):
        bengua_strs = self.ben_gua.__str__().split("\n")
        ben_gua_liuqin = []
        ben_gua_liuqin.extend(self.ben_gua.liu_qin)
        ben_gua_liuqin.reverse()
        s = "求测人年龄:%s 性别:%s 职业:%s\n" % (
            self.info['年龄'], self.info['性别'], self.info['职业'])
        for key in self.info:
            if key not in ['年龄', '性别', '职业']:
                if '时间' in key:
                    s += key + ":%s" % datetime.strptime(
                        self.info[key], "%Y/%m/%dT%H:%M:%S").strftime(
                        "%Y年%m月%d日%H点") + "\n"
                else:
                    s += key + ":%s" % self.info[key] + "\n"
        # s += "起卦时间：%s%s\n" % (self.nian, self.time)
        s += "\n"
        s += "排盘:\n"
        s += "\n"
        s += "%s年 %s月 %s日(%s空) %s卦" % (
            self.nian, self.yue, self.ri,
            "".join(i.name for i in self.kong_wang), self.code)
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
            # pyperclip.copy(s.replace("\t", "    "))
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
            # pyperclip.copy(s.replace("\t", "    "))
        s += "\n" + self.xiao_cheng_tu.tian_pan.__str__()
        return s

    def check_paipan_info(self):
        pass

    def get_ri_yue_shi_fen(self):
        pass

    def get_basic_info(self):
        pass


class PaiPanFromTime(PaiPan):
    def __init__(self, time="", nian="", yue="", ri="", shi="",
                 info=default_info, print_yin_yang=False):
        now = datetime.now()
        dizhis = "子丑寅卯辰巳午未申酉戌亥"
        dizhis_ = dizhis + "子"
        if time:
            now = datetime.strptime(time, '%Y-%m-%d %H')
        self.year, self.month, self.day, self.hour, self.shi_chen = \
            now.year, now.month, now.day, now.hour, \
            dizhis.index(dizhis_[math.ceil(now.hour / 2)]) + 1

        if not time:
            if re.match(r'^\d{4}$', nian):
                self.year = int(nian)
            if re.match(r'^\d{1,2}$', yue):
                self.month = int(yue)
            if re.match(r'^\d{1,2}$', ri):
                self.day = int(ri)
            if shi:
                if shi in dizhis:
                    self.shi_chen = dizhis.index(shi) + 1
                elif re.match(r'^\d+$', shi):
                    self.shi_chen = dizhis.index(
                        dizhis_[math.ceil(int(shi) / 2)]) + 1
                else:
                    print("输入的小时无效，应该输入24小时制的数字")
        code = self.get_time_code()
        super(PaiPanFromTime, self).__init__(code,
                                             info=info,
                                             print_yin_yang=print_yin_yang,
                                             nian=self.year,
                                             yue=self.month, )

    def get_time_code(self):
        s_num = self.year + self.month + self.day
        x_num = s_num + self.shi_chen
        shang_gua = s_num % 8
        if shang_gua == 0:
            shang_gua = 8
        xia_gua = x_num % 8
        if xia_gua == 0:
            xia_gua = 8
        dong_yao = xia_gua % 6
        if dong_yao == 0:
            dong_yao = 6
        return shang_gua * 100 + xia_gua * 10 + dong_yao


class PaiPanFromSentence(PaiPan):
    def __init__(self, chars, nian=0, yue=0, ri=0, shi="",
                 info=default_info, print_yin_yang=False):
        self.chars = chars
        if isinstance(shi, str):
            if not shi:
                self.shi = "子丑寅卯辰巳午未申酉戌亥".index(
                    "子丑寅卯辰巳午未申酉戌亥子"[math.ceil(datetime.now().hour / 2)]) + 1
            else:
                self.shi = "子丑寅卯辰巳午未申酉戌亥".index(shi) + 1
        elif isinstance(shi, int):
            self.shi = "子丑寅卯辰巳午未申酉戌亥".index(
                "子丑寅卯辰巳午未申酉戌亥子"[math.ceil(shi / 2)]) + 1
        self.strokes = self.get_stroke(chars)
        code = self.get_code(self.strokes, self.shi, nian, yue, ri)
        super(PaiPanFromSentence, self).__init__(code,
                                                 nian=nian,
                                                 yue=yue,
                                                 ri=ri,
                                                 shi=shi,
                                                 info=info,
                                                 print_yin_yang=print_yin_yang)

    def get_code(self, strokes, shi, nian=0, yue=0, ri=0):
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
                c_a_index = alphabets.index(char) + 1
                if c_a_index > 26:
                    c_a_index -= 26
                stroke_count_and_alphabet_index.append(c_a_index)
            elif char in nums:
                stroke_count_and_alphabet_index.append(nums.index(char))
            else:
                n = get_stroke(char)  # 括号等没有笔画
                if n:
                    stroke_count_and_alphabet_index.append(n)
        return stroke_count_and_alphabet_index

    def __str__(self):
        s = super(PaiPanFromSentence, self).__str__()
        s += "\n=============================\n"
        s += "字\t笔画\t和\t余数"
        s += "\n=============================\n"
        i = 0
        c = len(self.chars)
        count = 0
        t_count = 0
        for char in self.chars:
            count += self.strokes[i]
            t_count += self.strokes[i]
            if i == c // 2 - 1 or i == c - 1:
                s += "%s\t%s\t%s\t%s\n-----------------------------\n" % (
                    char, self.strokes[i], count, count % 8 if count % 8 else 8)
            else:
                s += "%s\t%s\t%s\n" % (char, self.strokes[i], count)
            if i == c // 2 - 1:
                count = 0
            i += 1
        t_count += self.shi
        s += "时辰\t%s\t%s\t\n-----------------------------\n" % (
            "子丑寅卯辰巳午未申酉戌亥"[self.shi - 1], self.shi)
        s += "总和\t\t%s\t%s\n=============================\n" % (
            t_count, t_count % 6 if t_count % 6 else 6)
        return s


class PaiPanFromTextAndTime(PaiPanFromSentence):
    def get_code(self, strokes, shi, nian, yue, ri):
        stroke_count = sum(strokes)
        nian_zhi_index = (nian - 1984 + 1) % 12
        if nian_zhi_index == 0:
            nian_zhi_index = 12

        shang_gua_count = nian_zhi_index + yue + ri + stroke_count
        xia_gua_count = shang_gua_count + shi
        shang_gua = shang_gua_count % 8
        xia_gua = xia_gua_count % 8
        dong_yao = xia_gua % 6
        if dong_yao == 0:
            dong_yao = 6
        if shang_gua == 0:
            shang_gua = 8
        if xia_gua == 0:
            xia_gua = 8
        return shang_gua * 100 + xia_gua * 10 + dong_yao

# print(Solar2LunarCalendar('2021/06/15'))
