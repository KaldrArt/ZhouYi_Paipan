from datetime import datetime, timedelta
import os
from common.calendar import get_jie_of_year, Solar2LunarCalendar
tiangan = '甲乙丙丁戊己庚辛壬癸'
dizhi = '子丑寅卯辰巳午未申酉戌亥'


def get_next_jiazi(current_jiazi):
    return tiangan[(tiangan.index(current_jiazi[0])+1) % 10] +\
        dizhi[(dizhi.index(current_jiazi[1])+1) % 12]


def get_previous_jiazi(current_jiazi):
    return tiangan[(tiangan.index(current_jiazi[0])-1) % 10] +\
        dizhi[(dizhi.index(current_jiazi[1])-1) % 12]


# print(get_next_jiazi('癸亥'))


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
    # ganzhi_of_previous_date = None
    print('需要解析的时间', date_to_parse)
    print('当天00:00的干支', ganzhi_of_date)
    jies = jie_around_date(date_to_parse)
    if jies['should_use_previous_date']:
        print("需要用到前一天的干支")
        # date_to_parse_previous_day = date_to_parse-timedelta(days=1)
        #date_str = date_to_parse_previous_day.strftime("%Y/%m/%d")
        # ganzhi_of_previous_date = list(Solar2LunarCalendar(date_str))
        # 优化，不需要通过ephem递归运算
        # ganzhi_of_date[0] = ganzhi_of_previous_date[0]
        # ganzhi_of_date[1] = ganzhi_of_previous_date[1]
        if jies['jie_after']['jie'][0] == '立春':
            # 修正正月初一才换年的问题
            # 因为原来的判断程序里，是根据正月初一换年的。
            # 如果当前不是正月、二月、三月、四月，那么立春的时候，是没有换年的，月要换成上一个月。
            # 如果当前是正月等，那么年已经提前换掉了，要换成之前的年。
            if jies['jie_after']['jie'][3].starts_with('正') or \
                    jies['jie_after']['jie'][3].starts_with('二') or \
                    jies['jie_after']['jie'][3].starts_with('三') or \
                    jies['jie_after']['jie'][3].starts_with('五') or \
                    jies['jie_after']['jie'][3].starts_with('四'):
                # 如果立春的时候，是正月初一，那么不变
                if jies['jie_after']['jie'][3] == '正月初一':
                    pass
                 # 如果立春的时候，已经是正月初一以后的时间，那么年干一定要向前减一年
                else:
                    ganzhi_of_date[0] = get_previous_jiazi(ganzhi_of_date[0])
                    pass
                pass
            elif jies['jie_after']['jie'][3].starts_with('九') or \
                    jies['jie_after']['jie'][3].starts_with('十') or \
                    jies['jie_after']['jie'][3].starts_with('八'):
                pass

            ganzhi_of_date[1] = get_previous_jiazi(ganzhi_of_date[1])
        # print('前一天00:00的干支', ganzhi_of_previous_date)
    if jies['should_use_next_day']:
        #date_to_parse_next_day = date_to_parse+timedelta(days=1)
        #date_str = date_to_parse_next_day.strftime("%Y/%m/%d")
        #ganzhi_of_next_date = list(Solar2LunarCalendar(date_str))
        # TODO: 可以优化，不需要递归来运算
        ganzhi_of_date[2] = get_next_jiazi(ganzhi_of_date[2])
    return ganzhi_of_date[0], ganzhi_of_date[1], ganzhi_of_date[2], ganzhi_of_date[3]


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
