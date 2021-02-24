import tushare as ts

# ts.set_token('c52c51a4cde56aa199146a3a6abe6e11d2a8607556c014b4ace4f4c5')
# ts.pro_bar('000591.SZ', start_date='20210224', end_date='20210224', freq='10min')

import baostock as bs
import pandas as pd

# bs.login()
# rs = bs.query_history_k_data_plus("sh.688059",
#                                   "date,code,open,high,low,close",
#                                   start_date='2021-02-14',
#                                   frequency="5", adjustflag="3")
# data_list = []
# while (rs.error_code == '0') & rs.next():
#     # 获取一条记录，将记录合并在一起
#     data_list.append(rs.get_row_data())
# result = pd.DataFrame(data_list, columns=rs.fields)
# result.to_csv("./history_A_stock_k_data_5m.csv", index=False)
# print(result)
