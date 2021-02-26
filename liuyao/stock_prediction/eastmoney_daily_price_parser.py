from datetime import datetime, timedelta


def excel_print(array):
    print("\t".join([str(i) for i in array[1]]))
    result = ['-']
    for i in range(1, len(array[1])):
        result.append(str(float(array[1][i]) - float(array[1][i - 1]))[0:6])
    print("\t".join(result))
    result = ['-']
    for i in range(1, len(array[1])):
        if float(array[1][i]) - float(array[1][i - 1]) > 0:
            result.append("↑")
        else:
            result.append("↓")
    print("\t".join(result))
    print("\t".join([str(i) for i in array[0]]))
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")


def localtime_to_meigutime(timestr="2021-02-24 22:30"):
    d = datetime.strptime(timestr, "%Y-%m-%d %H:%M") - timedelta(hours=13)
    return d.strftime("%Y-%m-%d %H:%M")


def east_money_json_to_data(data_array, mei_gu=False):
    result = []
    for d in data_array:
        dr = []
        ss = d.split(",")
        i = 0
        for s in ss:
            if mei_gu and i == 0:
                s = localtime_to_meigutime(s)
            dr.append(s)
            i += 1
        result.append(dr)
    return result


def input_to_di_zhi_shi_ke(data, zuo_shou_pan, meigu=False):
    shichen_data = [zuo_shou_pan]
    shichen = [["昨收", "开盘", '巳', '午', '未'], shichen_data]
    if meigu:
        shichen[0].append("申")
    last_data = zuo_shou_pan
    ke_data = []
    keling = [list('上子丑寅卯辰巳午未申酉戌亥'), ke_data]
    shichen_idx = 0
    kaipan_shichen = '巳午未申酉'
    for d in data:
        # 时辰的开始
        if '09:31' in d[0] or '11:01' in d[0] or "13:01" in d[0] or "15:01" in d[0]:
            ke_data = [last_data]
            if '09:31' in d[0]:
                keling = [list('上卯辰巳午未申酉戌亥'), ke_data]
            elif '11:01' in d[0]:
                dzlist = list('上子丑寅')
                if meigu:
                    dzlist = list('上子丑寅卯辰巳午未申酉戌亥')
                keling = [dzlist, ke_data]
            elif '15:01' in d[0]:
                keling = [list('上子丑寅卯辰巳'), ke_data]
            else:
                keling = [list('上子丑寅卯辰巳午未申酉戌亥'), ke_data]

        # 0是每一个刻令的末尾，但是要跳过9:30
        if d[0][-1] == "0" and d[0][-4:] != '9:30':
            # d[2]是这个刻令的末尾价格
            ke_data.append(d[2])

        # 00 是一个小时的最末尾一分钟的价格
        if meigu:
            end_time = "16:00"
        else:
            end_time = "15:00"
        if (('09:30' in d[0] or '11:00' in d[0] or "11:30" in d[0] or "15:00" in d[0]) and not meigu) or (
                meigu and (
                '09:30' in d[0] or '11:00' in d[0] or "16:00" in d[0] or "15:00" in d[0] or "13:00" in d[0])):
            shichen_data.append(d[2])
            if d[0][-4] != '9':
                print(kaipan_shichen[shichen_idx] + "时")
                excel_print(keling)
                shichen_idx += 1

        last_data = d[2]
    excel_print(shichen)


def input_to_fen(data, zuo_shou_pan, meigu=False):
    last_data = zuo_shou_pan
    fen_data = [zuo_shou_pan]
    fenling = [list('上子丑寅卯辰巳午未申酉戌亥'), fen_data]
    if meigu:
        index = '卯辰巳午未申酉戌亥子丑寅卯辰巳午未申酉戌亥子丑寅卯辰巳午未申酉戌亥子丑寅卯辰巳'
    else:
        index = "卯辰巳午未申酉戌亥子丑寅子丑寅卯辰巳午未申酉戌亥"

    last_info = ["09:30"]
    ii = 0
    shi = 2
    for d in data:
        m = d[0][-1]
        t = d[0][-5:]
        i = d[2]
        if m == "0" and d[0][-4:] != '9:30':
            fen_data.append(i)
            if index[ii] == "子":
                shi += 1
            print(index[shi] + "时" + index[ii] + "令" + last_info[0][-5:] + "至" + t)
            excel_print(fenling)
            last_info = d
            ii += 1
        elif m == "1":  # 子
            fen_data = [last_data]
            fen_data.append(i)
            fenling = [list('上子丑寅卯辰巳午未申酉戌亥'), fen_data]
        elif m in "37":  # 丑
            fen_data.append(i)
            fen_data.append(i)
        else:
            fen_data.append(i)
        last_data = i


def turn_input_to_liuyao(input, zuo_shou_pan, meigu=False):
    data = east_money_json_to_data(input, meigu)
    input_to_di_zhi_shi_ke(data, zuo_shou_pan, meigu)
    input_to_fen(data, zuo_shou_pan, meigu)
