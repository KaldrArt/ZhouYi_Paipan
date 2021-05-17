from liuyao.common.paipan.paipan import PaiPanFromSentence, PaiPanFromTime, PaiPan, normalize_num_code
import sys
import getopt
from datetime import datetime
import re
import pyperclip


def print_help():
    t = """
    举例：
    所测事项时间为2021年12月23日，卦码336，卦主年龄34，性别男，职业IT
    python qi_gua.py -t 2021-12-23T12 -n 336 -a 34 -r IT 
    
    参数说明：
    起卦内容参数：
        -t, --time      事项时间，即卦日月所在时间。如果不输入，则取起卦时间。无起卦时间则取当前时间。
                        格式 %Y-%m-%dT%H （可以用/替代-）, 例如：2021-12-23T12
        -c, --content   起卦内容，用于文字起卦，优先级最高。
        -n, --number    卦码起卦，优先级第二。
    
    卦主内容参数：
        -g, --gender    卦主性别，0女1男，F女M男，也可以直接输入男女。
        -a, --age       卦主年龄。
        -r, --role      卦主职业。
    
    详细设置卦所在时间和起卦时间参数：
        -s,-e, --setupTime 起卦时间，不指定则默认为当前时间。
                        格式 %Y-%m-%dT%H （可以用/替代-）, 例如：2021-12-23T12。
        -y, --year      卦年，数字。默认是起卦时间。如果输入-t则忽略本参数。
        -m, --month     卦月，数字。默认是起卦时间。如果输入-t则忽略本参数。
        -d, --day       卦日，数字。默认是起卦时间。如果输入-t则忽略本参数。
        -h, --hour      卦小时，数字，24小时制。默认是起卦时间。
    
        -p, --printBar  打印卦码，不需要加参数。
    """

    print(t)


def change_time_format(time_str):
    time_str = time_str.replace("/", "-")
    if re.match(r'^\d{4}-\d{1,2}-\d{1,2}T\d{1,2}$', time_str):
        return datetime.strptime(time_str, '%Y-%m-%dT%H')
    else:
        print("时间格式输入错误，取当前时间")
    return datetime.now()


def qi_gua(argv):
    now = datetime.now()
    year, month, day, hour = now.year, now.month, now.day, now.hour
    time = False
    setup_time_set = False
    setup_time = now
    content = ""
    number = ""
    info = {
        "年龄": "34", "性别": "男", "职业": "IT", "起卦时间": setup_time.strftime('%Y/%m/%dT%H:%M:%S')
    }
    only_help = False
    print_bar = False
    try:
        opts, args = getopt.getopt(argv, "m:d:c:h:n:y:t:pg:a:r:s:e",
                                   ["year=", "content=", "hour=", "month=", "day=", "number=", "time=", "printBar",
                                    "gender=", "age=", "role=", "setupTime=", "help"])
        if len(opts):
            for cmd, arg in opts:
                if cmd in ['--help']:
                    only_help = True
                    break
                elif cmd in ['-r', '--role']:
                    info['职业'] = arg
                elif cmd in ['-p', "--printBar"]:
                    print_bar = True
                elif cmd in ['-g', "--gender"]:
                    if arg in "01":
                        info['性别'] = "女男"[int(arg)]
                    elif arg in "FT":
                        info['性别'] = '女男'["FT".index(arg)]
                    elif arg in '男女':
                        info['性别'] = arg
                elif cmd in ['-a', "--age"]:
                    if re.match(r'^\d+$', arg):
                        info['年龄'] = arg
                elif cmd in ['-t', '--time']:
                    time = change_time_format(arg)
                    if time.year == year and time.month == month and time.day == day and time.hour == hour:
                        # 如果时间就是当前时间，那么置为False，也就是通过year等字段取值
                        time = False
                    else:
                        info['事项时间'] = time.strftime("%Y/%m/%dT%H:%M:%S")
                        year, month, day, hour = time.year, time.month, time.day, time.hour
                elif cmd in ['-s', '-e', "--setupTime"]:
                    if arg:
                        setup_time_set = True
                    setup_time = change_time_format(arg)
                    info["起卦时间"] = setup_time.strftime("%Y/%m/%dT%H:%M:%S")
                elif cmd in ['-m', '--month']:
                    month = arg
                elif cmd in ['-d', '--day']:
                    day = arg
                elif cmd in ['-h', "--hour"]:
                    hour = arg
                elif cmd in ['-c', '--content']:
                    content = arg
                    info['求测内容'] = content
                    info['起卦方式'] = '文字笔画起卦'
                elif cmd in ['-n', '--number']:
                    if re.match(r'^\d+$', arg):
                        number = int(arg)
                    info['起卦方式'] = '卦码起卦'
            if not time and setup_time_set:
                year, month, day, hour = setup_time.year, setup_time.month, setup_time.day, setup_time.hour
                print(year, month, day, hour)
        else:
            param = args[0]
            if re.match(r'^\d+$', param):
                number = param
                info['起卦方式'] = '卦码起卦'
            else:
                content = param
                info['求测内容'] = content
                info['起卦方式'] = '文字笔画起卦'
    except getopt.GetoptError as e:
        print("%s" % e)
    finally:
        if only_help:
            print_help()
        else:
            if content:
                gua = PaiPanFromSentence(chars=content, nian=year, yue=month, ri=day, shi=hour, info=info,
                                         print_yin_yang=print_bar)
                print(gua)
            elif number:
                gua = PaiPan(normalize_num_code(number), nian=year, yue=month, ri=day, shi=hour, info=info,
                             print_yin_yang=print_bar)
                print(gua)
            else:
                info['起卦方式'] = "根据事项时间起卦"
                # 如果设置了卦的时间
                if time:
                    gua = PaiPanFromTime(time=time.strftime("%Y-%m-%d %H"), info=info, print_yin_yang=print_bar)
                    print(gua)
                # 如果分开设置了卦的时间
                elif year and month and day and hour:
                    gua = PaiPanFromTime(nian=str(year), yue=str(month), ri=str(day), shi=str(hour), info=info,
                                         print_yin_yang=print_bar)
                    print(gua)
                # 如果时间无效
                else:
                    print("设置了无效时间")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print()
        qi_gua(sys.argv[1:])
    else:
        pyperclip.copy('python qi_gua.py -a 34 -r IT -g 1 ')
