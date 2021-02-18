from datetime import datetime
from common import di_zhi_list
from common.calendar import Solar2LunarCalendar
import math


class TimeGua:
    def __init__(self, init_input_number, calendar_type='solar'):
        self.datetime = datetime.now()
        self.lunar_time_tuple = Solar2LunarCalendar(self.datetime.strftime('%Y-%m-%d'))
        self.number = init_input_number
        self.shang_gua_number = self.shang_gua()
        self.xia_gua_number = self.xia_gua()
        self.dong_yao_number = self.dong_yao()
        print(self.shang_gua_number, self.xia_gua_number, self.dong_yao_number)

    def get_year_number(self):
        return di_zhi_list.index(self.lunar_time_tuple[0][1]) + 1

    def get_hour_number(self):
        index = math.ceil(self.datetime.hour / 2)
        if index == 12:
            index = 0
        return index + 1

    def shang_gua(self):
        result = (
                         self.get_year_number() +
                         self.datetime.month +
                         self.datetime.day +
                         self.number
                 ) % 8
        if result:
            return result
        else:
            return 8

    def xia_gua(self):
        result = (
                         self.shang_gua_number +
                         self.get_hour_number()
                 ) % 8
        if result:
            return result
        else:
            return 8

    def dong_yao(self):
        result = self.xia_gua_number % 6
        if result:
            return result
        else:
            return 6


print("前提：郑盛艳是我老婆的客户，没有做双录，可能会罚钱，客户态度又很差，媳妇很纠结怎么办")
print("用郑盛艳姓名笔画数起时空卦，客户郑盛艳什么时候会去宁波银行做双录？")
TimeGua(29)
