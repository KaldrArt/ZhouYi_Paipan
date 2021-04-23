import os
import csv
from common.database.stock import stock_info_collection, stock_daily_kline_collection
from datetime import datetime


class DataParser:
    """
    处理csv
    """
    file_path = os.getcwd().replace("run", "") + "liuyao/stock_prediction/shsz_data.CSV/"

    def __init__(self):
        self.stocks = self.get_stock_from_path()

    def get_stock_info(self):
        """
        获取每一个股票的信息
        :return:
        """
        pass

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
