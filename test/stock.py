import math


def profit(years=30, profit_rate=0.5, ding_tou=False, ding_tou_money=1):
    money = ding_tou_money * math.pow(1 + profit_rate, years)
    if ding_tou:
        for year in range(0, years):
            year_money = ding_tou_money * math.pow(1 + profit_rate, year)
            money += year_money
    return money


for pr in range(1, 20):
    p = profit(profit_rate=pr / 10, ding_tou=True, ding_tou_money=1)
    print("%s\t%d" % (pr / 10, p))
