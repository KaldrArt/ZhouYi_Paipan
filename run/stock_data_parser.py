from liuyao.stock_prediction.MGYD.data_parser import DataParser
from common.database.stock import stock_info_collection, stock_daily_kline_collection, error_collection, \
    finish_collection
from multiprocessing import Pool
from tqdm import tqdm
from liuyao.stock_prediction.MGYD.gua_generator import generate_gua
from common.calendar import Solar2LunarCalendar
import os

# dp = DataParser()

# dp.parse_data() #2021-04-23完成
# dp.get_stock_info() #2021-04-30完成
# dp.update_info_date() #20210502完成
# dp.update_kline_date() #2021-05-02完成


stocks = list(stock_info_collection.find({}, {"stock": 1, "name_history": 1, "type": 1}))
count = len(stocks)
finished = [i["stock"] for i in list(finish_collection.find({}))]


def get_kline_name_code(stock_id, date):
    stock_filter = filter(lambda x: x['stock'] == stock_id, stocks)
    if stock_filter:
        stock = list(stock_filter)[0]
        for h in stock['name_history']:
            if date >= h['start_date']:
                if h['end_date']:
                    if date < h['end_date']:
                        return {
                            "name": h["name"],
                            "code": h['code']
                        }
                else:
                    return {
                        "name": h["name"],
                        "code": h['code']
                    }
    return None


def update_stock_kline(i):
    stock = stocks[i]
    if stock['stock'] in finished:
        return
    # if not stock['stock'] == 'SH601975':
    #     return

    klines = list(
        stock_daily_kline_collection.find({"stock": stock['stock']},
                                          {"date": 1, "stock": 1, "open": 1, "high": 1, "low": 1,
                                           "close": 1, }).sort(
            "date"))
    for i in range(len(klines)):
        kline = klines[i]
        try:
            name_code = get_kline_name_code(kline['stock'], kline['date'])
            tian_gan_dizhi = Solar2LunarCalendar(kline['date'].strftime("%Y-%m-%d"))
            update_ob = {
                "cmpd2_tomorrow": None,
                "cmpd2_3days_after": None,
                "cmpd2_5days_after": None,
                "gua": generate_gua(kline, name_code['code']),
                "name_code": name_code,
                "gan_zhi": {
                    "nian": tian_gan_dizhi[0],
                    "yue": tian_gan_dizhi[1],
                    "ri": tian_gan_dizhi[2],
                    "nian_gan": tian_gan_dizhi[0][0],
                    "nian_zhi": tian_gan_dizhi[0][1],
                    "yue_gan": tian_gan_dizhi[1][0],
                    "yue_zhi": tian_gan_dizhi[1][1],
                    "ri_gan": tian_gan_dizhi[2][0],
                    "ri_zhi": tian_gan_dizhi[2][1]
                }
            }
            if i < len(klines) - 1:
                kline_tomorrow = klines[i + 1]
                if kline['close'] > kline_tomorrow['close']:
                    update_ob['cmpd2_tomorrow'] = -1
                elif kline['close'] == kline_tomorrow['close']:
                    update_ob['cmpd2_tomorrow'] = 0
                else:
                    update_ob['cmpd2_tomorrow'] = 1
            if i < len(klines) - 3:
                kline_3days_before = klines[i + 3]
                if kline['close'] > kline_3days_before['close']:
                    update_ob['cmpd2_3days_after'] = -1
                elif kline['close'] == kline_3days_before['close']:
                    update_ob['cmpd2_3days_after'] = 0
                else:
                    update_ob['cmpd2_3days_after'] = 1
            if i < len(klines) - 5:
                kline_5days_before = klines[i + 5]
                if kline['close'] > kline_5days_before['close']:
                    update_ob['cmpd2_5days_after'] = -1
                elif kline['close'] == kline_5days_before['close']:
                    update_ob['cmpd2_5days_after'] = 0
                else:
                    update_ob['cmpd2_5days_after'] = 1
            stock_daily_kline_collection.update_one({"_id": kline['_id']}, {"$set": update_ob})
        except Exception as err:
            error_collection.insert({"kline_id": kline["_id"], "err": err.__str__()})
    finish_collection.insert({"stock": stock['stock'], "i": i})


# count = 20
if __name__ == '__main__':
    with Pool(8) as p:
        r = list(tqdm(p.imap(update_stock_kline, range(count)), total=count))
