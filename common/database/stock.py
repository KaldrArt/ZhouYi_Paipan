from pymongo import MongoClient
from common.database.config import uri

client = MongoClient(uri)
stock_db = client.get_database('stock_liuyao')

stock_info_collection = stock_db.get_collection("stock_info")
stock_daily_kline_collection = stock_db.get_collection("stock_daily_kline")
