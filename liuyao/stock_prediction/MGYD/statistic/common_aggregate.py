from bazi_common.database.stock import stock_daily_kline_collection


class CommonAggregate:
    gua_type = ['price', 'code_price', "name_code_price"]
    gua_sub_type = ['normal', 'unicode']
    gua_children_type = [
        'today_open', 'today_open_by_point',  # 今天的开盘价预测今天的走势
        'today_close', 'today_close_by_point',  # 今天的开票价预测明天的走势
        'today_high', 'today_high_by_point',  # 今天的最高价，预测明天的走势
        'today_low', 'today_low_by_point',  # 今天的最低价，预测明天的走势
        'today_open_and_close',  # 今天的开盘价和收盘价，预测明天的走势
        'today_high_and_low'  # 今天的最高价和最低价，预测明天的走势
    ]
    pass
