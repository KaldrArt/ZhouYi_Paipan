from liuyao.xiaochengtu.xiaochengtu import XiaoChengTu, get_xiao_cheng_tu_from_4_codes, get_xiao_cheng_tu_from_gua_code
from liuyao.common.gua import SanYaoGua
import math

gua_list = "乾兑离震巽坎艮坤"


def get_gua_code_from_price(price):
    up, down = str(price).split(".")
    if down == "00":
        price_str = str(math.ceil(price))
        split_bit = len(price_str) // 2
        up = price_str[0:split_bit]
        down = price_str[split_bit:]
    shang_gua_count = 0
    for b in up:
        shang_gua_count += int(b)
    xia_gua_count = 0
    for b in down:
        xia_gua_count += int(b)
    shang_gua = shang_gua_count % 8
    xia_gua = xia_gua_count % 8
    if shang_gua == 0:
        shang_gua = 8
    if xia_gua == 0:
        xia_gua = 8
    return shang_gua * 10 + xia_gua


def get_gua_by_shang_xia_box(zhang, has_shang, has_xia):
    if zhang:
        if has_shang and has_xia:
            result = 6
        elif has_shang and not has_xia:
            result = 2
        elif not has_shang and has_xia:
            result = 5
        else:
            result = 1
    else:
        if has_shang and has_xia:
            result = 3
        elif has_shang and not has_xia:
            result = 7
        elif not has_shang and has_xia:
            result = 4
        else:
            result = 8
    return SanYaoGua[gua_list[result - 1]]


def get_yong_shen_gua_from_k_line(open_price, close, high, low):
    has_shang = False
    has_xia = False
    zhang = False
    if open_price > close:
        # 跌，阴块
        if high > open_price:
            has_shang = True
        if low < close:
            has_xia = True
    elif open_price < close:
        zhang = True
        # 涨，阳块
        if high > close:
            has_shang = True
        if low < open_price:
            has_xia = True
    else:
        if high > open_price:
            has_shang = True
        if low < open_price:
            has_xia = True
        if high - open_price > open_price - low:
            zhang = True
        elif high - open_price < open_price - low:
            zhang = False
        else:
            zhang = False
    return get_gua_by_shang_xia_box(zhang, has_shang, has_xia)


class PriceToXiaoChengTu:
    def __init__(self, open_price, close, high, low):
        self.open = open_price
        self.close = close
        self.high = high
        self.low = low
        self.xiao_cheng_tu: XiaoChengTu = self.get_xiaochengtu_from_k_line()
        self.xiao_cheng_tu.print_tian_pan()
        self.yongshen = self.get_yongshen()

    def get_yongshen(self):
        yongshen = get_yong_shen_gua_from_k_line(self.open, self.close, self.high, self.low)
        print("\n用神：\n")
        print(yongshen.value)
        return yongshen

    def get_xiaochengtu_from_k_line(self) -> XiaoChengTu:
        ben_gua_code = get_gua_code_from_price(self.open)
        bian_gua_code = get_gua_code_from_price(self.close)
        return get_xiao_cheng_tu_from_gua_code(ben_gua_code, bian_gua_code)


# 创业板
# 9-17
PriceToXiaoChengTu(3124.31, 3193.26, 3201.45, 3122.32)
