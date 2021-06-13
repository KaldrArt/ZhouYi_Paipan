from datetime import datetime, timedelta
import os
from common.calendar import get_jie_of_year, Solar2LunarCalendar


def mkdir(folder):
    if os.path.exists(folder):
        return True
    else:
        os.mkdir(folder)


def jie_around_date(date: datetime):
    """
    根据当前时间，来看当前天跟十二节的情况
    返回前一个节气和后一个节气，以及与前后两个节之间的时间间隔，用秒代表，如果当前时刻比上一个节气小于1天，那么将should_be_next_month置为true
    比如12:30换节，那么12:31比上一个节气小于1天，那么应该是下一个月了，因此时间上按照下一天来建
    """
    year = date.year
    month = date.month
    jieqis = get_jie_of_year(year)
    if month == 1:
        jieqis = get_jie_of_year(year-1)+jieqis
    elif month == 12:
        jieqis += get_jie_of_year(year+1)
    last_jie = None
    current_jie = None
    next_jie = None
    for jie in jieqis:
        if date < jie[1]:
            last_jie = current_jie
            next_jie = jie
            break
        current_jie = jie
    pre_jie_time_diff = date-last_jie[1]
    next_jie_time_diff = next_jie[1]-date
    result = {
        'jie_before': {
            'jie': last_jie,
            'diff_seconds': pre_jie_time_diff.seconds
        },
        'jie_after': {
            'jie': next_jie,
            'diff_seconds': next_jie_time_diff.seconds
        },
        "should_use_previous_date": False,
        'should_use_next_day': True if date.hour == 23 else False
    }
    """
    只有和后一个换节气在同一天，才需要比较，否则不需要。
    不需要和前一个节气比较，因为当前算法如果当天含有节气，就直接算在下一个月了。
    0~23:应按照上一天的年、月，日、时辰不变。
        比如当前时间13:15，下一个换节气时间是13:18，13:18以前日、时辰都不变，只是年月变了。
    23~23:59:59:应按照前一天的年、月、日则正确，时辰不变。
        比如当前时间是23:50，换节气时间是23:30，那么日应该按下一天00:00来计算，月n年也是如此。
    """
    if date.year == next_jie[1].year and \
            date.month == next_jie[1].month and \
            date.day == next_jie[1].day:
        result['should_use_previous_date'] = True
    return result


def get_gan_zhi_of_date(date):
    if isinstance(date, datetime):
        date_to_parse = date
    else:
        date = date.replace("/", "-").replace(" ", "T")
        if "T" not in date:
            date += "T00:00"
        year_str, month_str, day_str = date.split("T")[0].split("-")
        hour_str, minute_str = date.split("T")[1].split(":")
        date_to_parse = datetime(
            int(year_str), int(month_str), int(day_str),
            int(hour_str), int(minute_str)
        )
    date_str = date_to_parse.strftime("%Y/%m/%d")
    ganzhi_of_date = list(Solar2LunarCalendar(date_str))
    ganzhi_of_previous_date = None
    print(date_to_parse)
    print('当天00:00的干支', ganzhi_of_date)
    jies = jie_around_date(date_to_parse)
    if jies['should_use_previous_date']:
        print("需要用到前一天的干支")
        date_to_parse_previous_day = date_to_parse-timedelta(days=1)
        date_str = date_to_parse_previous_day.strftime("%Y/%m/%d")
        ganzhi_of_previous_date = list(Solar2LunarCalendar(date_str))
        # TODO: 可以优化，不需要递归运算
        ganzhi_of_date[0] = ganzhi_of_previous_date[0]
        ganzhi_of_date[1] = ganzhi_of_previous_date[1]
        print('前一天00:00的干支', ganzhi_of_previous_date)
    if jies['should_use_next_day']:
        date_to_parse_next_day = date_to_parse+timedelta(days=1)
        date_str = date_to_parse_next_day.strftime("%Y/%m/%d")
        ganzhi_of_next_date = list(Solar2LunarCalendar(date_str))
        # TODO: 可以优化，不需要递归来运算
        ganzhi_of_date[2] = ganzhi_of_next_date[2]
    return ganzhi_of_date[0], ganzhi_of_date[1], ganzhi_of_date[2], ganzhi_of_date[3]


jies = get_jie_of_year(2020)
for jie in jies:
    print("====================================")
    print(jie)
    time_before = jie[1]-timedelta(days=1)
    print("-------节气之前1天-------")
    print('原结果', time_before, Solar2LunarCalendar(
        time_before.strftime("%Y/%m/%d %H:%M")))
    print('转换', get_gan_zhi_of_date(time_before))
    print("\n-------节气之前1分钟-------")
    t = (jie[1]-timedelta(seconds=1*60)).strftime("%Y/%m/%d %H:%M")
    print("原结果", t, Solar2LunarCalendar(t))
    print('转换', get_gan_zhi_of_date(t))
    print("\n-------节气之后1分钟-------")
    t = (jie[1]+timedelta(minutes=1)).strftime("%Y/%m/%d %H:%M")
    print("原结果", t, Solar2LunarCalendar(t))
    print('转换', get_gan_zhi_of_date(t))
    time_after = jie[1]+timedelta(days=1)
    print("\n-------节气之后1天-------")
    print('节气之后1天的转换结果', time_after, get_gan_zhi_of_date(
        time_after.strftime("%Y/%m/%d %H:%M")))


def init_date(date: str):
    date = date.replace("/", "-")
    if " " in date or "T" in date:
        date = date.replace(" ", "T")
        year_str, month_str, day_str = date.split("T")[0].split("-")
    else:
        year_str, month_str, day_str = date.split("-")
    year = int(year_str)
    month = int(month_str)
    day = int(day_str)
    if ":" in date:
        date = date.replace(" ", "T")
        hour_after_str = date.split("T")[1]
        hour_after_str_list = hour_after_str.split(":")
        if len(hour_after_str_list) == 3:
            hour = int(hour_after_str_list[0])
            minute = int(hour_after_str_list[1])
            second = int(hour_after_str_list[2])
        elif len(hour_after_str_list) == 2:
            hour = int(hour_after_str_list[0])
            minute = int(hour_after_str_list[1])
            second = 0
        else:
            hour = 0
            minute = 0
            second = 0
    else:
        hour = 0
        minute = 0
        second = 0
    parsed_date = datetime(year, month, day, hour, minute, second)
    if hour >= 23:
        lunar_date = parsed_date + timedelta(hours=1)
    else:
        lunar_date = parsed_date
    lunar_date_str = lunar_date.strftime("%Y/%m/%d")
    return parsed_date, lunar_date_str, lunar_date
