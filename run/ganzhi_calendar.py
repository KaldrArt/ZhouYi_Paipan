from bazi_common.ganzhi_calendar.calendar import Calendar
import getopt
import sys
from datetime import datetime


def print_help():
    t = """
    参数说明：
        -h, --help      显示帮助
        -y, --year      起始年，默认为当年
        -m, --month     起始月，默认为当月
        -s, --span      输出的月的数量，默认输出1个月的数量
                        如果指定-y或--year参数，则输出至少12个月的数据
        -b, --by_year   输出全年

    举例：
    
    输出一年的数据：
        python ganzhi_calendar.py --year=2021
        python ganzhi_calendar.py -y 2023
        python ganzhi_calendar.py -y
    
    输出本月1个月的数据：
        python ganzhi_calendar.py
    
    输出从2021年4月开始，共4个月的日历
        python ganzhi_calendar.py -y 2021 -m 4 -s 4

    """
    print(t)


def show_calendar(argv):
    today = datetime.now()
    year = today.year
    month = today.month
    by_year = False
    month_spans = 1
    only_help = False
    try:
        opts, args = getopt.getopt(argv, "hs:m:y:b",
                                   ["year=", "span=", "month=", "help", "by_year"])
        if len(opts):
            for cmd, arg in opts:
                if cmd in ['--help', '-h']:
                    only_help = True
                    break
                elif cmd in ['-y', '--year']:
                    year = int(arg)
                elif cmd in ['-m', '--month']:
                    if 1 <= int(arg) <= 12:
                        month = int(arg)
                elif cmd in ['--span', '-s']:
                    if int(arg) > month_spans:
                        month_spans = int(arg)
                elif cmd in ['-b', "--by_year"]:
                    by_year = True
    except getopt.GetoptError as e:
        print("%s" % e)
    finally:
        if only_help:
            print_help()
        else:
            Calendar(
                year=year,
                month=month,
                month_spans=month_spans,
                by_year=by_year
            )


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print()
        show_calendar(sys.argv[1:])
    else:
        print()
        Calendar(month=datetime.now().month, month_spans=1)
