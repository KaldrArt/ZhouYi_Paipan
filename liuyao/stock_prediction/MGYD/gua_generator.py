from common.database.stock import stock_daily_kline_collection, stock_info_collection, stock_gua_by_price_collection, \
    error_collection
from .utils import get_stock_shu

stock_info_list = list(stock_info_collection.find({}, {
    "stock_name": 1,
    "type": 1,
    "name_history": 1,
    "stock": 1
}))
stock_info = {}
for i in stock_info_list:
    stock_info[i['stock']] = i


def get_shu_from_base(base, unicode=False):
    result = {}
    for key in base:
        shang_gua_base, xia_gua_base = base[key]
        shang_gua_shu = 0
        dong_yao = 0
        for char in shang_gua_base:
            shang_gua_shu += ord(char) if unicode else int(char)
        dong_yao += shang_gua_shu
        shang_gua_shu = shang_gua_shu % 8
        if shang_gua_shu == 0:
            shang_gua_shu = 8
        xia_gua_shu = 0
        for char in xia_gua_base:
            xia_gua_shu += ord(char) if unicode else int(char)
        dong_yao += xia_gua_shu
        xia_gua_shu = xia_gua_shu % 8
        if xia_gua_shu == 0:
            xia_gua_shu = 8
        dong_yao = dong_yao % 6
        if dong_yao == 0:
            dong_yao = 6
        result[key] = "%s%s%s" % (shang_gua_shu, xia_gua_shu, dong_yao)
    return result


def get_normal_shu_from_base(base):
    return get_shu_from_base(base)


def get_unicode_shu_from_base(base):
    return get_shu_from_base(base, True)


def split_price_by_point(price):
    if price < 50:
        price *= 10
    strs = str(price).split(".")
    return strs[0], strs[1]


def split_price_by_position(price):
    strs = str(price).replace(".", "")
    c = len(strs) // 2
    return strs[0:c], strs[c:]


def generate_price_gua(kline):
    # 按照小数点划分 by_point结尾
    # 按照小数点划分的，如果是指数，则正常划分，如果不是指数，那么需要先乘以10再划分，例如7.12，如果一直是7左右，那么上卦就不会变了，而末尾的变动是比较多的，因此不怕
    # 按照小数点划分，开盘50以下，小数点向后移一位，50以上不改小数点
    # 按照数字的整数+小数位数划分（这样有一个问题，就是整数位可能永远是一样的），按照
    # unicode和normal两种方式
    base = {
        "today_open": split_price_by_position(kline['open']),
        "today_open_by_point": split_price_by_point(kline['open']),
        "today_close": split_price_by_position(kline['close']),
        "today_close_by_point": split_price_by_point(kline['close']),
        "today_high": split_price_by_position(kline['high']),
        "today_high_by_point": split_price_by_point(kline['high']),
        "today_low": split_price_by_position(kline['low']),
        "today_low_by_point": split_price_by_point(kline['low']),
        "today_open_and_close": (str(kline['open']).replace(".", ""), str(kline['close']).replace(".", "")),
        "today_high_and_low": (str(kline['high']).replace(".", ""), str(kline['low']).replace(".", "")),
    }
    normal = get_normal_shu_from_base(base)
    # unicode = get_unicode_shu_from_base(base)
    return {
        "normal": normal,
        # "unicode": unicode
    }


def __get_gua_from_codes(code_list):
    split_position = len(code_list) // 2
    shang_gua = sum(code_list[0:split_position]) % 8
    xia_gua = sum(code_list[split_position:]) % 8
    bian_yao = (sum(code_list[0:split_position]) + sum(code_list[split_position:])) % 6
    if shang_gua == 0:
        shang_gua = 8
    if xia_gua == 0:
        xia_gua = 8
    if bian_yao == 0:
        bian_yao = 6
    return shang_gua, xia_gua, bian_yao


def __get_new_gua_with_code(old_gua_code, new_codes):
    old_shang_gua = int(old_gua_code[0])
    old_xia_gua = int(old_gua_code[1])
    old_bian_yao = int(old_gua_code[2])
    new_shang_gua, new_xia_gua, new_bian_yao = __get_gua_from_codes(new_codes)
    shang_gua = (old_shang_gua + new_shang_gua) % 8
    if shang_gua == 0:
        shang_gua = 8
    xia_gua = (old_xia_gua + new_xia_gua) % 8
    if xia_gua == 0:
        xia_gua = 8
    bian_yao = (old_bian_yao + new_bian_yao) % 6
    if bian_yao == 0:
        bian_yao = 6
    return "%s%s%s" % (shang_gua, xia_gua, bian_yao)


def __generate_gua_with_another(gua, child_code):
    result = {}
    for key in gua:
        result[key] = __get_new_gua_with_code(gua[key], child_code)
    return result


def generate_code_price_gua(pre_gua, stock_id_code, with_unicode=False):
    # 编码可以按照位数直接拆分为上下
    result = {
        "normal": __generate_gua_with_another(pre_gua['normal'], stock_id_code['basic_count'])
    }
    if with_unicode:
        result["unicode"] = __generate_gua_with_another(pre_gua['normal'], stock_id_code['unicode_count']),
    return result


def generate_name_code_price_gua(pre_gua, stock_name_code):
    return generate_code_price_gua(pre_gua, stock_name_code, with_unicode=True)


def generate_gua(kline, name_code):
    price_gua = generate_price_gua(kline)
    code_price_gua = generate_code_price_gua(price_gua, name_code['stock_id'])
    return {
        "price": price_gua,
        "code_price": code_price_gua,
        'name_code_price': generate_name_code_price_gua(code_price_gua, name_code['stock_name'])
    }


class GuaGenerator:
    limit = 1000
    generate_type = 1

    def __init__(self, i):
        self.i = i
        data = self.get_data()
        self.insert_data(data)

    def get_data(self):
        fields = {"open": 1, "high": 1, "low": 1, "close": 1, "stock": 1, 'date': 1, "volume": 1,
                  "outstanding_share": 1}
        data = list(
            stock_daily_kline_collection.find({}, {"fields": fields}).skip(self.i * self.limit).limit(self.limit))
        return data

    def insert_data(self, data):
        for d in data:
            if self.generate_type == 1:
                price_gua = generate_price_gua(d)
                code_price_gua = generate_code_price_gua(d)
                name_code_price_gua = generate_name_code_price_gua(d)
                d['price_gua'] = price_gua
                d['code_price_gua'] = code_price_gua
                d['name_code_price_gua'] = name_code_price_gua
        stock_gua_by_price_collection.insert_many(data)
