import os
import csv
from common.database.stock import stock_info_collection, stock_daily_kline_collection, tushare_info, \
    stock_name_code_collection
from datetime import datetime
import baostock
import tushare
from liuyao.stock_prediction.MGYD.utils import get_stock_shu
import time
from tqdm import tqdm
from pprint import pprint


class DataParser:
    """
    处理csv
    """
    file_path = os.getcwd().replace("run", "") + "liuyao/stock_prediction/shsz_data.CSV/"

    def __init__(self):
        self.stocks = self.get_stock_from_path()

    def get_stock_info(self):
        """
        获取股票的信息
        :return:
        """
        result = {}
        n = len(self.stocks)
        baostock.login()
        tushare.set_token(tushare_info['token'])
        pro = tushare.pro_api()
        i = 0
        for j in tqdm(range(len(self.stocks))):
            stock = self.stocks[j]
            time.sleep(3)
            rs = baostock.query_stock_basic("%s.%s" % (stock[1], stock[2]))
            nc = pro.namechange(ts_code='%s.%s' % (stock[2], stock[1]))
            # 打印结果集
            data_list = []
            while (rs.error_code == '0') & rs.next():
                # 获取一条记录，将记录合并在一起
                data_list.append(rs.get_row_data())
            if data_list:
                stock_info = data_list[0]
                data = {
                    "stock": stock[0],
                    'bao_stock_id': stock_info[0],
                    'stock_name': stock_info[1],
                    'ipo_date': datetime.strptime(stock_info[2], "%Y-%m-%d"),
                    'out_date': None if not stock_info[3] else None,
                    'type': int(stock_info[4]),
                    'status': int(stock_info[5]),
                    'name_history': nc.to_dict('records')
                }
                stock_info_collection.update_one({"stock": data['stock']}, {"$set": data}, upsert=True)
            i += 1
            # sys.stdout.flush()
            # print("%s-%s/%s" % (stock[0], i, n))
        baostock.logout()
        return result

    def get_stock_from_path(self):
        """
        通过路径获取所有股票
        :return:
        """
        files = os.listdir(self.file_path)
        stocks = []
        for filename in files:
            filename = filename.replace(".csv", "")
            if filename.startswith("SZ"):
                stocks.append((filename, "SZ", filename[2:]))
            elif filename.startswith("SH"):
                stocks.append((filename, "SH", filename[2:]))
        return stocks

    def parse_data(self):
        """
        获取股票的信息
        :return:
        """
        result = {}
        n = len(self.stocks)
        i = 0
        for stock in self.stocks:
            self.parse_file(stock[2], stock[1])
            i += 1
            print("%s-%s/%s" % (stock[0], i, n))
        return result

    def parse_file(self, stock_id="000001", stock_type="SH"):
        titles = ['date', 'open', 'high', 'low', 'close', 'volume', 'outstanding_share']
        filename = "%s%s%s.csv" % (self.file_path, stock_type, stock_id)
        with open(filename) as file:
            for row in csv.DictReader(file, fieldnames=titles):
                row['stock_area'] = stock_type
                row['stock_id'] = stock_id
                row["stock"] = stock_type + stock_id
                row['date'] = row['date']
                row['high'] = float(row['high'])
                row['low'] = float(row['low'])
                row['close'] = float(row['close'])
                row['open'] = float(row['open'])
                row['volume'] = float(row['volume'])
                row['outstanding_share'] = float(row['outstanding_share'])
                stock_daily_kline_collection.insert(row)

    def parse_stock_name_code(self):
        cursor = stock_info_collection.find({})
        for stock in cursor:
            if stock["name_history"]:
                # 正常股票，都有历史，起始和终止时间很重要
                pass
            else:
                # 指数等，没有改名历史
                pass

    def update_date(self):
        # self.update_info_date() #20210502完成
        # self.update_kline_date() #20210502完成
        pass

    def update_kline_date(self):
        limit = 10000
        kline_count = stock_daily_kline_collection.count({})
        count = kline_count // limit + 1
        for i in tqdm(range(count)):
            cursor = stock_daily_kline_collection.find({}).skip(i * limit).limit(limit)
            for item in cursor:
                formatted_date = datetime.strptime(item['date'], "%Y/%m/%d")
                stock_daily_kline_collection.update({"_id": item["_id"]}, {"$set": {"date": formatted_date}})

    def update_info_date(self):
        cursor = list(stock_info_collection.find({}))
        for i in tqdm(range(len(cursor))):
            item = cursor[i]
            history = []
            if item['name_history']:
                for h in item['name_history']:
                    h['code'] = get_stock_shu(h['name'], item["stock"])
                    if isinstance(h['start_date'], str):
                        h['start_date'] = datetime.strptime(h['start_date'], '%Y%m%d')
                        h['ann_date'] = datetime.strptime(h['ann_date'], '%Y%m%d') if h['ann_date'] else None
                    history.append(h)
            self.rebuild_history(history)
            stock_info_collection.update({"_id": item["_id"]}, {"$set": {"name_history": history}})

    def rebuild_history(self, history_list):
        history_list.sort(key=lambda k: k.get("start_date", 0), reverse=False)
        for i in range(len(history_list) - 1):
            history_list[i]['end_date'] = history_list[i + 1]['start_date']
