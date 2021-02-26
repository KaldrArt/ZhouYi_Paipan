from datetime import datetime


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
