from liuyao.common.zh_dict.stroke import get_stroke
from common.database.stock import stock_info_collection
from liuyao.stock_prediction.MGYD.utils import get_stock_name_strokes

cursor = stock_info_collection.find({})
for item in cursor:
    print(item['stock_name'])
    
    print(get_stroke("逼"))
