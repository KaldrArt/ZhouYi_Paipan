from datetime import datetime, timedelta
from common.calendar import Solar2LunarCalendar, get_jie_of_year
from colorama import Fore, Back, Style

jie_qi_list = ["立春",
               "惊蛰",
               "清明",
               "立夏",
               "芒种",
               "小暑",
               "立秋",
               "白露",
               "寒露",
               "立冬",
               "大雪",
               "小寒"]


class Theme:
    def __init__(self, theme="normal"):
        self.year_empty = Back.RESET + Fore.RESET
        self.title_1 = Back.RESET + Fore.RESET
        self.title_0 = Back.RESET + Fore.RESET
        self.workday_1 = Back.RESET + Fore.RESET
        self.workday_0 = Back.RESET + Fore.RESET
        self.weekend_1 = Back.RESET + Fore.RESET
        self.weekend_0 = Back.RESET + Fore.RESET
        self.month_start = Back.RESET + Fore.RESET
        self.gan_zhi_yue_start = Back.RESET + Fore.RESET
        self.flag = Back.RESET + Fore.RESET
        self.qi_flag = Back.RESET + Fore.RESET
        self.qi = Back.RESET + Fore.RESET
        self.jia = Back.RESET + Fore.RESET
        self.zi = Back.RESET + Fore.RESET
        self.today = Back.RESET + Fore.RESET
        self.today_symbol = Back.RESET + Fore.RESET
        self.end_separator = Back.RESET + Fore.RESET
        self.start_separator = Back.RESET + Fore.RESET
        self.get_theme(theme)

    def get_theme(self, theme="normal"):
        if theme == "normal":
            self.normal_theme()

    def normal_theme(self):
        self.year_empty = Back.BLACK
        self.title_1 = Back.LIGHTBLUE_EX + Fore.LIGHTWHITE_EX
        self.title_0 = Back.BLUE + Fore.LIGHTWHITE_EX
        self.workday_1 = Back.LIGHTYELLOW_EX + Fore.BLACK
        self.workday_0 = Back.YELLOW + Fore.BLACK
        self.weekend_1 = Back.LIGHTBLACK_EX + Fore.BLACK
        self.weekend_0 = Back.LIGHTBLACK_EX + Fore.BLACK
        self.month_start = Back.BLACK + Fore.WHITE
        self.gan_zhi_yue_start = Back.RED + Fore.WHITE
        self.flag = Back.RESET + Fore.RED
        self.qi_flag = Back.RESET + Fore.LIGHTRED_EX
        self.qi = Back.LIGHTRED_EX + Fore.WHITE
        self.jia = Back.GREEN + Fore.BLACK
        self.zi = Back.BLUE + Fore.WHITE
        self.today = Back.LIGHTMAGENTA_EX + Fore.WHITE
        self.today_symbol = Fore.LIGHTMAGENTA_EX
        self.end_separator = Back.LIGHTBLUE_EX
        self.start_separator = Back.BLUE


class Calendar:
    theme = Theme()

    def __init__(self,
                 year=datetime.now().year,
                 month=1,
                 month_spans=12,
                 calendar_type="地支",
                 by_year=False,
                 simple=False):
        self.index = 1
        self.month = month
        self.year = year
        self.month_spans = month_spans
        self.tiangan_list = list("甲乙丙丁戊己庚辛壬癸")
        self.dizhi_list = list("子丑寅卯辰巳午未申酉戌亥")
        self.calendar_type = calendar_type
        if calendar_type == "天干":
            self.titles = self.tiangan_list
            char_index = 0
        else:
            self.titles = self.dizhi_list
            char_index = 1
        self.simple = simple
        self.by_year = by_year
        self.first_day_in_this_year = datetime(year, 1, 1)
        self.first_day_of_this_month = datetime(year, month, 1)
        self.jie_qi = get_jie_of_year(year, False) + get_jie_of_year(year + 1, False)
        self.first_day_of_month_tuple = Solar2LunarCalendar(self.first_day_of_this_month)
        self.first_day_tuple = Solar2LunarCalendar(self.first_day_in_this_year)
        self.year_left_null = self.titles.index(self.first_day_tuple[2][char_index])
        self.month_left_null = self.titles.index(self.first_day_of_month_tuple[2][char_index])
        self.print(by_year=by_year)

    def get_char(self, text="", day=datetime.now(),
                 title=False, empty_char=False, print_type="shell",
                 need_gan_zhi_notify=False, line_end_jie=False, line_end_qi=False, qi=False, jia_notify=False,
                 zi_notify=False):
        char = ""
        if print_type == "shell":
            if empty_char:
                char += self.theme.year_empty + "  "
                if not self.simple:
                    char += "  "
            elif line_end_jie:
                char += self.theme.end_separator + " " + \
                        self.theme.qi + " " + text.split("/")[0] + self.theme.qi_flag + Back.RED + "" + \
                        self.theme.gan_zhi_yue_start + text.split("/")[1] + " " + self.theme.flag + ""
            elif line_end_qi:
                char += self.theme.end_separator + " " + self.theme.qi + " " + text + " " + self.theme.qi_flag + ""
            elif title:
                char += self.theme.__getattribute__("title_%s" % (self.index % 2)) + " " + text + " "
            else:
                today = False
                separate_symbol_left = " "
                separate_symbol_right = " "
                if day.year == datetime.now().year and day.month == datetime.now().month and day.day == datetime.now().day:
                    today = True
                    separate_symbol_left = self.theme.today_symbol + ""
                    separate_symbol_right = self.theme.today_symbol + ""
                if day.day == 1:
                    month = day.month
                    if month < 10:
                        month = "0" + str(month)
                    else:
                        month = str(month)
                    char += self.theme.month_start + " %s " % ("  " if self.simple else month)
                else:
                    if need_gan_zhi_notify:
                        char += self.theme.gan_zhi_yue_start + separate_symbol_left + (
                            self.theme.today if today else "") + text + self.theme.gan_zhi_yue_start + separate_symbol_right
                    else:
                        if qi:
                            char += self.theme.qi
                        elif day.weekday() < 5:
                            char += self.theme.__getattribute__("workday_%s" % (self.index % 2))
                        # weekend start
                        elif day.weekday() in [5, 6]:
                            char += self.theme.__getattribute__("workday_%s" % (self.index % 2))
                        if day.weekday() == 6:
                            date = "日"
                        # elif day.weekday() == 5:
                        #     date = "六"
                        elif day.day < 10:
                            date = "0" + str(day.day)
                        else:
                            date = str(day.day)
                        if jia_notify and self.calendar_type != "天干":
                            char += self.theme.jia
                        elif zi_notify and self.calendar_type == "天干":
                            char += self.theme.zi
                        if today:
                            separate_symbol_left = char + separate_symbol_left
                            separate_symbol_right = char + separate_symbol_right
                            date = self.theme.today + str(date)
                        char += "  " if self.simple else separate_symbol_left + date + separate_symbol_right
        if not line_end_jie and not line_end_qi:
            self.index += 1
        # if self.index % len(self.titles) == 0:
        #     self.index += 1
        return char + Style.RESET_ALL

    def print(self,
              by_year=False,
              print_type="shell"):
        if by_year:
            lines = self.print_year(print_type=print_type)
        else:
            lines = self.print_months(max_months=self.month_spans,
                                      first_day_tuple=self.first_day_of_month_tuple,
                                      left_null_span=self.month_left_null,
                                      print_type=print_type,
                                      first_day=self.first_day_of_this_month)
        for line in lines:
            if len(line) == 12:
                line.append(self.theme.end_separator + " " + Fore.RESET + Back.RESET)
            line.insert(0, "\t" + self.theme.start_separator + " " + Fore.RESET + Back.RESET)
            print("".join(line))

    def print_months(self,
                     max_months=12,
                     first_day_tuple=(),
                     left_null_span=0,
                     print_type='shell',
                     first_day=None):
        max_months += 1
        if not first_day_tuple:
            first_day_tuple = self.first_day_tuple
            left_null_span = self.year_left_null
        if not first_day:
            first_day = self.first_day_in_this_year
        lines = [[self.get_char(text=c, title=True) for c in self.titles]]
        column_count = len(self.titles)
        current_month = self.month
        calculated_months = 1
        line = []
        first_day_month_gan_index = self.tiangan_list.index(first_day_tuple[1][0])
        current_month_gan_index = first_day_month_gan_index
        current_month_zhi = first_day_tuple[1][1]
        for k in range(left_null_span):
            line.append(self.get_char(empty_char=True))
        line_end_jie = False
        line_end_qi = False
        current_jieqi = self.jie_qi[0]
        first_day_tiangan_index = self.tiangan_list.index(first_day_tuple[2][0])
        first_day_dizhi_index = self.dizhi_list.index(first_day_tuple[2][1])
        gan_zhi_month = ""
        gan_zhi_month_dizhi = ""
        for i in range(365 * 3):
            day = first_day + timedelta(days=i)
            day_gan_index = (first_day_tiangan_index + i) % 10
            day_zhi_index = (first_day_dizhi_index + i) % 12
            day_gan = self.tiangan_list[day_gan_index]
            day_zhi = self.dizhi_list[day_zhi_index]
            jia_notify = False
            zi_notify = False
            if day_gan == "甲":
                jia_notify = True
            if day_zhi == "子":
                zi_notify = True
            need_gan_zhi_notify = False
            need_qi = False
            for jie_qi in self.jie_qi:
                if day.year == jie_qi[1].year and day.month == jie_qi[1].month and day.day == jie_qi[1].day:
                    current_jieqi = jie_qi
                    if current_jieqi[0] in jie_qi_list:
                        line_end_jie = True
                        need_gan_zhi_notify = True
                        gan_zhi_month_dizhi = self.dizhi_list[(jie_qi_list.index(current_jieqi[0]) + 2) % 12]
                        if current_month_zhi != gan_zhi_month_dizhi:
                            current_month_gan_index += 1
                            current_month_gan_index %= 10
                            current_month_zhi = gan_zhi_month_dizhi
                        gan_zhi_month = self.tiangan_list[current_month_gan_index] + gan_zhi_month_dizhi
                    else:
                        line_end_qi = True
                        gan_zhi_month = ""
                        need_qi = True
                    break
            if (12 >= current_month != day.month) or (
                    current_month > 12 and current_month - 12 != day.month):
                current_month += 1
                calculated_months += 1
            if (i + left_null_span + 1) % column_count == 0 or calculated_months == max_months:
                if calculated_months != max_months:
                    line.append(self.get_char(day=day, print_type=print_type,
                                              need_gan_zhi_notify=need_gan_zhi_notify,
                                              qi=need_qi,
                                              text=gan_zhi_month_dizhi,
                                              jia_notify=jia_notify,
                                              zi_notify=zi_notify))
                else:
                    if line:
                        for k in range(12 - len(line)):
                            line.append(self.get_char(empty_char=True))
                if line_end_jie or line_end_qi:
                    jieqi_str = current_jieqi[0] + current_jieqi[1].strftime("%H:%M")
                    line.append(
                        self.get_char(
                            text="%s / %s月" % (jieqi_str, gan_zhi_month) if gan_zhi_month else "%s" % jieqi_str,
                            print_type=print_type,
                            line_end_jie=line_end_jie,
                            line_end_qi=line_end_qi))
                    line_end_jie = False
                    line_end_qi = False
                if line:
                    lines.append(line)
                # if (current_month % 12 in [3, 6, 9, 0] and (
                #         19 <= day.day <= 31) and max_months >= 7) and calculated_months < max_months - 1:
                #     lines.append([self.get_char(text=c, title=True) for c in self.titles])
                line = []
            else:
                line.append(self.get_char(day=day, print_type=print_type,
                                          need_gan_zhi_notify=need_gan_zhi_notify,
                                          qi=need_qi,
                                          text=gan_zhi_month_dizhi,
                                          jia_notify=jia_notify,
                                          zi_notify=zi_notify))

            if calculated_months == max_months:
                break
        lines.append([self.get_char(text=c, title=True) for c in self.titles])
        # lines.append([self.get_char(text="  ", title=True) for c in self.titles])
        return lines

    def print_year(self, print_type='shell'):
        max_months = 12
        if self.month_spans > max_months:
            max_months = self.month_spans
        return self.print_months(
            first_day_tuple=self.first_day_of_month_tuple,
            left_null_span=self.month_left_null,
            first_day=self.first_day_of_this_month,
            max_months=max_months,
            print_type=print_type)
