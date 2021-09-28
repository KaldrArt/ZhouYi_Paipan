import sys
import getopt


def print_help():
    t = """
    举例：
    通过卦码起卦
    python qi_xiaochengtu.py  -n 3362 -c 本次疗休养团的情况
    
    通过本卦、之卦起卦
    python qi_xiaochengtu.py -b 履 -z 晋 -c 本次活动是否顺利
    
    参数说明：
    起卦内容参数：
        -c, --content       起卦内容。
        -n, --number        卦码起卦。
        -b, --ben           本卦
        -z, --zhi           之卦
        --help              显示帮助
    """

    print(t)


def qi_xiaochengtu(argv):
    try:
        pass
    except getopt.GetoptError as e:
        print("%s" % e)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print()
        qi_xiaochengtu(sys.argv[1:])
    else:
        pass
