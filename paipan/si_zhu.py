from common.calendar import Solar2LunarCalendar
from common.jiazi import JiaZi, JiaZiBase
from datetime import datetime, timedelta
from common import *
import math


def init_date(date: str):
    date = date.replace("/", "-")
    if " " in date or "T" in date:
        date = date.replace(" ", "T")
        year_str, month_str, day_str = date.split("T")[0].split("-")
    else:
        year_str, month_str, day_str = date.split("-")
    year = int(year_str)
    month = int(month_str)
    day = int(day_str)
    if ":" in date:
        date = date.replace(" ", "T")
        hour_after_str = date.split("T")[1]
        hour_after_str_list = hour_after_str.split(":")
        if len(hour_after_str_list) == 3:
            hour = int(hour_after_str_list[0])
            minute = int(hour_after_str_list[1])
            second = int(hour_after_str_list[2])
        elif len(hour_after_str_list) == 2:
            hour = int(hour_after_str_list[0])
            minute = int(hour_after_str_list[1])
            second = 0
        else:
            hour = 0
            minute = 0
            second = 0
    else:
        hour = 0
        minute = 0
        second = 0
    parsed_date = datetime(year, month, day, hour, minute, second)
    if hour >= 23:
        lunar_date = parsed_date + timedelta(hours=1)
    else:
        lunar_date = parsed_date
    lunar_date_str = lunar_date.strftime("%Y/%m/%d")
    return parsed_date, lunar_date_str


class SiZhu:
    def __init__(self, date, gender=True, solar=True):
        self.solar = True or solar
        self.date, self.solar_to_lunar_date = init_date(date)
        self.gender = gender
        if self.solar:
            self.nian, self.yue, self.ri, self.yinli = Solar2LunarCalendar(self.solar_to_lunar_date)

        self.nian_zhu: JiaZiBase = JiaZi[self.nian].value
        self.yue_zhu: JiaZiBase = JiaZi[self.yue].value
        self.ri_zhu: JiaZiBase = JiaZi[self.ri].value
        self.shi_zhu: JiaZiBase = self.get_shi_zhu()
        self.kong_wang = self.ri_zhu.kong_wang
        self.shi = self.shi_zhu.name
        self.yinli = self.get_yinli_str()
        self.bazi = self.get_bazi()

    def get_yinli_str(self):
        return "%s年%s%s时" % (self.nian, self.yinli, self.shi_zhu.name)

    def get_bazi(self):
        return "%s造: %s%s %s%s %s%s %s%s (%s%s)" % (
            "乾" if self.gender else "坤",
            self.nian_zhu.tian_gan.name,
            self.nian_zhu.di_zhi.name,
            self.yue_zhu.tian_gan.name,
            self.yue_zhu.di_zhi.name,
            self.ri_zhu.tian_gan.name,
            self.ri_zhu.di_zhi.name,
            self.shi_zhu.tian_gan.name,
            self.shi_zhu.di_zhi.name,
            self.kong_wang[0].name,
            self.kong_wang[1].name
        )

    def get_shi_zhu(self) -> JiaZiBase:
        hour = self.date.hour
        if hour == 23:
            dizhi_index = 0
        else:
            dizhi_index = math.ceil(hour / 2)
        if dizhi_index > 11:
            dizhi_index -= 12
        shi_chen = di_zhi_list[dizhi_index]
        shi_chen_tian_gan_start = "壬"
        if self.ri_zhu.tian_gan.name in ["甲", "己"]:
            shi_chen_tian_gan_start = "甲"
        elif self.ri_zhu.tian_gan.name in ['乙', '庚']:
            shi_chen_tian_gan_start = "丙"
        elif self.ri_zhu.tian_gan.name in ["丙", '辛']:
            shi_chen_tian_gan_start = "戊"
        elif self.ri_zhu.tian_gan.name in ["丁", '壬']:
            shi_chen_tian_gan_start = "庚"
        shi_chen_tian_gan_index = (tian_gan_list.index(shi_chen_tian_gan_start) + dizhi_index) % 10
        shi_chen_tian_gan = tian_gan_list[shi_chen_tian_gan_index]
        return JiaZi["%s%s" % (shi_chen_tian_gan, shi_chen)].value
