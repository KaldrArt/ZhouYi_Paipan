from bazi_common.database.stock import statistic_gua_with_price_collection, stock_daily_kline_collection, \
    statistic_gua_with_ri_yue_collection, stock_db

pipeline = [
    {
        '$group': {
            '_id': {
                'tomorrow': '$cmpd2_tomorrow',
                'gua': '$gua.name_code_price.normal.today_open_and_close',
                "yue_zhi": "$gan_zhi.yue_zhi",
                "ri_zhi": "$gan_zhi.ri_zhi",
            },
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'tomorrow': '$_id.tomorrow',
            'yue': '$_id.yue_zhi',
            'ri': '$_id.ri_zhi',
            'gua': '$_id.gua',
            'count': 1
        }
    }, {
        '$out': 'statistic_gua_with_ri_yue'
    }
]
# stock_daily_kline_collection.aggregate(pipeline, allowDiskUse=True)

gua_list = list(statistic_gua_with_ri_yue_collection.find({}))
gua_prediction = {}

for item in gua_list:

    if 'gua' not in item:
        continue
    gua_name = item['gua'] + item['yue'] + item['ri']
    if gua_name not in gua_prediction:
        gua_prediction[gua_name] = {
            "up": 0,
            "down": 0,
            "draw": 0,
            'count': 0
        }
    if item['tomorrow'] == 1:
        gua_prediction[gua_name]["up"] += item['count']
    elif item['tomorrow'] == -1:
        gua_prediction[gua_name]["down"] += item['count']
    else:
        gua_prediction[gua_name]["draw"] += item['count']
    gua_prediction[gua_name]['count'] += item['count']

for gua in gua_prediction:
    p = gua_prediction[gua]
    print("%s\t%s\t%s\t%.2f%%\t%.2f%%\t%.2f%%\t%s" % (
        gua[0:3], gua[3], gua[4], p['up'] / p['count'] * 100, p['down'] / p['count'] * 100,
        p['draw'] / p['count'] * 100,
        p['count']))
