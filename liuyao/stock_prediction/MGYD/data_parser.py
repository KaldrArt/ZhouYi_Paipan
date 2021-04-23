import os
import csv
from common.database.stock import stock_info_collection, stock_daily_kline_collection, tushare_info
from datetime import datetime
import baostock
import tushare


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
        # tushare.set_token(tushare_info['token'])
        # pro = tushare.pro_api()
        i = 0
        for stock in self.stocks:
            rs = baostock.query_stock_basic("%s.%s" % (stock[1], stock[2]))
            # nc = pro.namechange(ts_code='%s.%s' % (stock[2], stock[1]))
            # print(nc)
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
                    'name_history': []
                }
                stock_info_collection.update_one({"stock": data['stock']}, data, upsert=True)
            i += 1
            print("%s-%s/%s" % (stock[0], i, n))
            break
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
