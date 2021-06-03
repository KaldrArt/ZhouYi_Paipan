from datetime import datetime, timedelta
from common.calendar import Solar2LunarCalendar, get_jie_of_year
from colorama import init, Fore, Back, Style

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
    def __init__(self):
        self.year_empty = Back.LIGHTBLACK_EX
        self.title_1 = Back.LIGHTBLUE_EX + Fore.LIGHTWHITE_EX
        self.title_0 = Back.BLUE + Fore.LIGHTWHITE_EX
        self.workday_1 = Back.LIGHTYELLOW_EX + Fore.BLACK
        self.workday_0 = Back.YELLOW + Fore.BLACK
        self.weekend_1 = Back.LIGHTBLACK_EX + Fore.WHITE
        self.weekend_0 = Back.LIGHTBLACK_EX + Fore.WHITE
        self.month_start = Back.BLACK + Fore.WHITE
        self.gan_zhi_yue_start = Back.RED + Fore.WHITE
        self.flag = Back.RESET + Fore.RED


class Calendar:
    first_day_in_this_year = datetime(datetime.now().year, 1, 1)
    first_day_of_this_month = datetime(datetime.now().year, datetime.now().month, 1)
    jie_qi = get_jie_of_year(datetime.now().year) + get_jie_of_year(datetime.now().year + 1)
    theme = Theme()

    def __init__(self, calendar_type="地支", simple=False):
        self.index = 0
        if calendar_type == "天干":
            self.titles = list("甲乙丙丁戊己庚辛壬癸")
            char_index = 0
        else:
            self.titles = list("子丑寅卯辰巳午未申酉戌亥")
            char_index = 1
        self.simple = simple
        self.first_day_tuple = Solar2LunarCalendar(self.first_day_in_this_year)
        self.year_left_null = self.titles.index(self.first_day_tuple[2][char_index])

    def print(self, start=datetime.now(), end=datetime.now() + timedelta(days=30), print_type="shell"):
        pass

    def get_char(self, text="", day=datetime.now(), title=False, empty_char=False, print_type="shell",
                 need_gan_zhi_notify=False, line_end_jie_qi=False):
        char = ""
        if print_type == "shell":
            if empty_char:
                char += self.theme.year_empty + "  "
                if not self.simple:
                    char += "  "
            elif line_end_jie_qi:
                char += self.theme.gan_zhi_yue_start + " " + text + " " + self.theme.flag + ""
            elif title:
                char += self.theme.__getattribute__("title_%s" % (self.index % 2)) + " " + text + " "
            else:
                if day.day == 1:
                    month = day.month
                    if month < 10:
                        month = "0" + str(month)
                    else:
                        month = str(month)
                    char += self.theme.month_start + " %s " % ("  " if self.simple else month)
                else:
                    if need_gan_zhi_notify:
                        char += self.theme.gan_zhi_yue_start + " " + text + " "
                    else:
                        if day.weekday() < 5:
                            char += self.theme.__getattribute__("workday_%s" % (self.index % 2))
                        # weekend start
                        elif day.weekday() in [5, 6]:
                            char += self.theme.__getattribute__("workday_%s" % (self.index % 2))
                        if day.weekday() == 6:
                            date = "日"
                        elif day.weekday() == 5:
                            date = "六"
                        elif day.day < 10:
                            date = "0" + str(day.day)
                        else:
                            date = str(day.day)
                        char += "  " if self.simple else " " + str(date) + " "
        if not line_end_jie_qi:
            self.index += 1
        # if self.index % len(self.titles) == 0:
        #     self.index += 1
        return char + Style.RESET_ALL

    def print_year(self, print_type='shell'):
        max_months = 25
        lines = ["".join([self.get_char(text=c, title=True) for c in self.titles])]
        column_count = len(self.titles)
        current_month = 1
        line = []
        for k in range(self.year_left_null):
            line.append(self.get_char(empty_char=True))
        line_end_jie_qi = False
        current_jieqi = self.jie_qi[0]
        gan_zhi_month = ""
        for i in range(365 * 3):
            day = self.first_day_in_this_year + timedelta(days=i)
            need_gan_zhi_notify = False
            for jie_qi in self.jie_qi:
                if day.year == jie_qi[1].year and day.month == jie_qi[1].month and day.day == jie_qi[1].day:
                    need_gan_zhi_notify = True
                    line_end_jie_qi = True
                    current_jieqi = jie_qi
                    gan_zhi_month = "寅卯辰巳午未申酉戌亥子丑"[jie_qi_list.index(current_jieqi[0])]
                    break
            if (12 >= current_month != day.month) or (
                    current_month > 12 and current_month - 12 != day.month):
                current_month += 1
            if (i + self.year_left_null + 1) % column_count == 0 or current_month == max_months:
                if current_month != max_months:
                    line.append(self.get_char(day=day, print_type=print_type, need_gan_zhi_notify=need_gan_zhi_notify,
                                              text=gan_zhi_month))
                if line_end_jie_qi:
                    line.append(
                        self.get_char(
                            text="%s/%s月" % (current_jieqi[0], gan_zhi_month),
                            print_type=print_type,
                            line_end_jie_qi=line_end_jie_qi))
                    line_end_jie_qi = False
                if line:
                    lines.append("".join(line))
                if day.month in [3, 6, 9, 12] and (19 <= day.day <= 31) and current_month < max_months - 1:
                    lines.append("".join([self.get_char(text=c, title=True) for c in self.titles]))
                line = []
            else:
                line.append(self.get_char(day=day, print_type=print_type, need_gan_zhi_notify=need_gan_zhi_notify,
                                          text=gan_zhi_month))

            if current_month == max_months:
                break
        lines.append("".join([self.get_char(text=c, title=True) for c in self.titles]))
        for line in lines:
            print(line)
