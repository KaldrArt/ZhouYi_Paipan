from pymongo import MongoClient
from common.database.config import uri

client = MongoClient(uri)
stock_db = client.get_database('stock_liuyao')
tushare_info = {
    "token": "c52c51a4cde56aa199146a3a6abe6e11d2a8607556c014b4ace4f4c5",
    'username': '18618124986',
    "password": 'ivy2498'
}

stock_info_collection = stock_db.get_collection("stock_info")
stock_daily_kline_collection = stock_db.get_collection("stock_daily_kline")
