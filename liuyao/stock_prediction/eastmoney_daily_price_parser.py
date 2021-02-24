def excel_print(array):
    for item in array:
        print("\t".join([str(i) for i in item]))
    result = ['-']
    for i in range(1, len(array[1])):
        if float(array[1][i]) - float(array[1][i - 1]) > 0:
            result.append("↑")
        else:
            result.append("↓")
    print("\t".join(result))


def east_money_json_to_data(data_array):
    result = []
    for d in data_array:
        dr = []
        ss = d.split(",")
        for s in ss:
            dr.append(s)
        result.append(dr)
    return result


def input_to_di_zhi_shi_ke(data, zuo_shou_pan):
    shichen_data = [zuo_shou_pan]
    shichen = [["昨收", "开盘", '巳', '午', '未'], shichen_data]
    last_data = zuo_shou_pan
    ke_data = []
    keling = [list('上子丑寅卯辰巳午未申酉戌亥'), ke_data]
    for d in data:
        # 时辰的开始
        if '09:31' in d[0] or '11:01' in d[0] or "13:01" in d[0]:
            ke_data = [last_data]
            if '09:31' in d[0]:
                keling = [list('上卯辰巳午未申酉戌亥'), ke_data]
            elif '11:01' in d[0]:
                keling = [list('上子丑寅'), ke_data]
            else:
                keling = [list('上子丑寅卯辰巳午未申酉戌亥'), ke_data]

        # 0是每一个刻令的末尾，但是要跳过9:30
        if d[0][-1] == "0" and d[0][-4:] != '9:30':
            # d[2]是这个刻令的末尾价格
            ke_data.append(d[2])

        # 00 是一个小时的最末尾一分钟的价格
        if '09:30' in d[0] or '11:00' in d[0] or "11:30" in d[0] or "15:00" in d[0]:
            shichen_data.append(d[2])
            if d[0][-4] != '9':
                excel_print(keling)
        last_data = d[2]
    excel_print(shichen)


def input_to_fen(data, zuo_shou_pan):
    last_data = zuo_shou_pan
    fen_data = [zuo_shou_pan]
    fenling = [list('上子丑寅卯辰巳午未申酉戌亥'), fen_data]
    index = '卯辰巳午未申酉戌亥子丑寅子丑寅卯辰巳午未申酉戌亥'
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


def turn_input_to_liuyao(input, zuo_shou_pan):
    data = east_money_json_to_data(input)
    input_to_di_zhi_shi_ke(data, zuo_shou_pan)
    input_to_fen(data, zuo_shou_pan)


data20210224 = ["2021-02-24 09:30,6.80,6.80,6.80,6.80,46073,31329816.00,6.800",
                "2021-02-24 09:31,6.80,6.85,6.88,6.75,113448,77374295.00,6.814",
                "2021-02-24 09:32,6.85,6.81,6.86,6.81,59912,40912147.00,6.818",
                "2021-02-24 09:33,6.81,6.88,6.91,6.81,62830,43183267.00,6.831",
                "2021-02-24 09:34,6.89,6.88,6.89,6.87,35666,24529744.00,6.836",
                "2021-02-24 09:35,6.87,6.86,6.89,6.86,28350,19492887.00,6.839",
                "2021-02-24 09:36,6.84,6.71,6.84,6.71,45820,31058846.00,6.832",
                "2021-02-24 09:37,6.70,6.78,6.79,6.70,41499,27938319.00,6.822",
                "2021-02-24 09:38,6.77,6.80,6.80,6.77,28010,18995675.00,6.820",
                "2021-02-24 09:39,6.82,6.78,6.82,6.78,19286,13122093.00,6.819",
                "2021-02-24 09:40,6.78,6.73,6.78,6.73,25206,17023853.00,6.816",
                "2021-02-24 09:41,6.74,6.78,6.79,6.73,18141,12257375.00,6.814",
                "2021-02-24 09:42,6.78,6.82,6.84,6.77,19161,13023089.00,6.813",
                "2021-02-24 09:43,6.83,6.87,6.88,6.83,28753,19726845.00,6.816",
                "2021-02-24 09:44,6.87,6.92,6.92,6.86,30375,20915440.00,6.819",
                "2021-02-24 09:45,6.93,6.90,6.94,6.89,35440,24505301.00,6.825",
                "2021-02-24 09:46,6.89,6.93,6.94,6.89,34890,24121431.00,6.829",
                "2021-02-24 09:47,6.93,6.88,6.93,6.88,34589,23892492.00,6.833",
                "2021-02-24 09:48,6.89,6.91,6.91,6.88,24884,17164355.00,6.835",
                "2021-02-24 09:49,6.90,6.89,6.90,6.88,21745,14987460.00,6.837",
                "2021-02-24 09:50,6.88,6.87,6.88,6.85,12641,8679875.00,6.837",
                "2021-02-24 09:51,6.86,6.90,6.90,6.86,14837,10217724.00,6.838",
                "2021-02-24 09:52,6.89,6.87,6.89,6.87,10044,6911888.00,6.839",
                "2021-02-24 09:53,6.87,6.89,6.89,6.87,9099,6263837.00,6.839",
                "2021-02-24 09:54,6.89,6.88,6.89,6.88,9513,6550799.00,6.840",
                "2021-02-24 09:55,6.87,6.88,6.88,6.87,8905,6125669.00,6.840",
                "2021-02-24 09:56,6.87,6.83,6.87,6.83,15440,10583401.00,6.841",
                "2021-02-24 09:57,6.82,6.84,6.85,6.82,10331,7061423.00,6.841",
                "2021-02-24 09:58,6.85,6.87,6.87,6.84,5677,3888892.00,6.841",
                "2021-02-24 09:59,6.86,6.85,6.87,6.85,9676,6639044.00,6.841",
                "2021-02-24 10:00,6.85,6.85,6.86,6.84,7909,5419828.00,6.841",
                "2021-02-24 10:01,6.85,6.87,6.87,6.84,18282,12554567.00,6.842",
                "2021-02-24 10:02,6.88,6.92,6.93,6.88,39254,27105055.00,6.844",
                "2021-02-24 10:03,6.93,6.91,6.95,6.90,33707,23345944.00,6.847",
                "2021-02-24 10:04,6.91,6.91,6.91,6.90,12914,8917721.00,6.848",
                "2021-02-24 10:05,6.90,6.90,6.91,6.88,8583,5920721.00,6.848",
                "2021-02-24 10:06,6.89,6.92,6.92,6.89,15303,10567190.00,6.849",
                "2021-02-24 10:07,6.92,6.98,6.98,6.92,29351,20401488.00,6.852",
                "2021-02-24 10:08,6.99,6.98,7.00,6.96,65462,45706523.00,6.860",
                "2021-02-24 10:09,6.98,7.01,7.04,6.98,65012,45609651.00,6.869",
                "2021-02-24 10:10,7.02,6.99,7.02,6.99,46556,32652246.00,6.874",
                "2021-02-24 10:11,7.01,7.09,7.09,7.00,36464,25698039.00,6.879",
                "2021-02-24 10:12,7.10,7.18,7.20,7.10,77595,55528405.00,6.896",
                "2021-02-24 10:13,7.19,7.13,7.19,7.09,58228,41581145.00,6.906",
                "2021-02-24 10:14,7.12,7.12,7.18,7.10,48853,34926629.00,6.914",
                "2021-02-24 10:15,7.11,7.06,7.11,7.03,32966,23348555.00,6.918",
                "2021-02-24 10:16,7.03,7.11,7.11,7.03,14772,10452480.00,6.920",
                "2021-02-24 10:17,7.11,7.06,7.12,7.06,24215,17173968.00,6.923",
                "2021-02-24 10:18,7.05,7.06,7.07,7.05,14179,10000250.00,6.924",
                "2021-02-24 10:19,7.06,7.07,7.08,7.05,12821,9062465.00,6.925",
                "2021-02-24 10:20,7.07,7.09,7.09,7.07,10380,7351495.00,6.926",
                "2021-02-24 10:21,7.09,7.10,7.10,7.09,11706,8296905.00,6.927",
                "2021-02-24 10:22,7.09,7.08,7.10,7.08,10792,7653520.00,6.929",
                "2021-02-24 10:23,7.07,7.03,7.07,7.03,14733,10389984.00,6.930",
                "2021-02-24 10:24,7.02,7.00,7.03,7.00,14954,10482900.00,6.930",
                "2021-02-24 10:25,7.00,7.01,7.01,6.99,16305,11406238.00,6.931",
                "2021-02-24 10:26,7.01,7.05,7.06,7.01,8790,6192045.00,6.932",
                "2021-02-24 10:27,7.05,7.03,7.06,7.03,13058,9201498.00,6.933",
                "2021-02-24 10:28,7.03,7.02,7.03,7.01,10013,7025967.00,6.933",
                "2021-02-24 10:29,7.02,7.03,7.03,7.01,5100,3581414.00,6.933",
                "2021-02-24 10:30,7.03,7.04,7.04,7.03,7502,5279633.00,6.934",
                "2021-02-24 10:31,7.05,7.02,7.05,7.02,10024,7049696.00,6.935",
                "2021-02-24 10:32,7.02,7.02,7.03,7.02,7062,4960727.00,6.935",
                "2021-02-24 10:33,7.03,7.03,7.03,7.02,6733,4726039.00,6.935",
                "2021-02-24 10:34,7.03,7.02,7.03,7.02,6951,4882582.00,6.936",
                "2021-02-24 10:35,7.02,7.04,7.04,7.02,4971,3491769.00,6.936",
                "2021-02-24 10:36,7.04,7.05,7.05,7.03,5412,3810478.00,6.936",
                "2021-02-24 10:37,7.05,7.06,7.06,7.04,6319,4454261.00,6.937",
                "2021-02-24 10:38,7.06,7.09,7.09,7.06,7372,5212367.00,6.937",
                "2021-02-24 10:39,7.09,7.12,7.12,7.09,12511,8880927.00,6.938",
                "2021-02-24 10:40,7.11,7.09,7.12,7.09,9750,6925571.00,6.939",
                "2021-02-24 10:41,7.08,7.05,7.08,7.05,7359,5200467.00,6.940",
                "2021-02-24 10:42,7.05,7.06,7.06,7.04,5773,4070764.00,6.940",
                "2021-02-24 10:43,7.05,7.07,7.07,7.05,4777,3375891.00,6.941",
                "2021-02-24 10:44,7.06,7.06,7.07,7.06,4732,3343224.00,6.941",
                "2021-02-24 10:45,7.06,7.06,7.06,7.05,4457,3144412.00,6.941",
                "2021-02-24 10:46,7.06,7.05,7.06,7.05,3685,2599770.00,6.941",
                "2021-02-24 10:47,7.05,7.02,7.05,7.02,7858,5525630.00,6.942",
                "2021-02-24 10:48,7.03,7.03,7.04,7.02,6422,4514146.00,6.942",
                "2021-02-24 10:49,7.04,7.03,7.04,7.03,3888,2733950.00,6.942",
                "2021-02-24 10:50,7.03,7.02,7.04,7.02,5457,3836221.00,6.943",
                "2021-02-24 10:51,7.03,7.01,7.03,7.01,4914,3450868.00,6.943",
                "2021-02-24 10:52,7.01,6.97,7.01,6.97,18618,13021441.00,6.943",
                "2021-02-24 10:53,6.97,6.93,6.97,6.93,11541,8020257.00,6.943",
                "2021-02-24 10:54,6.92,6.86,6.92,6.86,18316,12631551.00,6.943",
                "2021-02-24 10:55,6.86,6.91,6.91,6.85,15059,10347315.00,6.942",
                "2021-02-24 10:56,6.93,6.93,6.95,6.92,10824,7502596.00,6.942",
                "2021-02-24 10:57,6.93,6.92,6.94,6.92,9989,6922664.00,6.942",
                "2021-02-24 10:58,6.93,6.96,6.96,6.93,5446,3778600.00,6.942",
                "2021-02-24 10:59,6.96,6.99,6.99,6.96,6253,4362599.00,6.942",
                "2021-02-24 11:00,6.99,7.00,7.01,6.99,7628,5337359.00,6.943",
                "2021-02-24 11:01,6.99,6.97,6.99,6.96,4707,3286548.00,6.943",
                "2021-02-24 11:02,6.97,6.98,6.99,6.97,5060,3526749.00,6.943",
                "2021-02-24 11:03,6.97,6.99,6.99,6.97,2973,2075492.00,6.943",
                "2021-02-24 11:04,6.99,6.98,7.00,6.98,7129,4981851.00,6.943",
                "2021-02-24 11:05,6.99,6.96,6.99,6.96,4944,3445362.00,6.943",
                "2021-02-24 11:06,6.96,6.93,6.96,6.93,4122,2860249.00,6.943",
                "2021-02-24 11:07,6.93,6.94,6.95,6.92,3734,2588439.00,6.943",
                "2021-02-24 11:08,6.94,6.94,6.95,6.93,5359,3717398.00,6.943",
                "2021-02-24 11:09,6.94,6.93,6.94,6.93,4027,2791831.00,6.943",
                "2021-02-24 11:10,6.94,6.93,6.94,6.93,3844,2665316.00,6.943",
                "2021-02-24 11:11,6.93,6.89,6.94,6.88,14577,10071981.00,6.943",
                "2021-02-24 11:12,6.88,6.88,6.89,6.88,5244,3610265.00,6.943",
                "2021-02-24 11:13,6.89,6.90,6.90,6.88,4274,2945587.00,6.942",
                "2021-02-24 11:14,6.90,6.89,6.90,6.89,5381,3710390.00,6.942",
                "2021-02-24 11:15,6.90,6.90,6.90,6.89,5351,3692349.00,6.942",
                "2021-02-24 11:16,6.90,6.89,6.91,6.89,6948,4791754.00,6.942",
                "2021-02-24 11:17,6.90,6.89,6.90,6.88,8729,6015989.00,6.942",
                "2021-02-24 11:18,6.88,6.89,6.90,6.88,3833,2640863.00,6.942",
                "2021-02-24 11:19,6.90,6.90,6.90,6.89,2401,1655962.00,6.942",
                "2021-02-24 11:20,6.89,6.90,6.91,6.89,4630,3195414.00,6.942",
                "2021-02-24 11:21,6.91,6.93,6.93,6.90,3849,2661961.00,6.941",
                "2021-02-24 11:22,6.93,6.95,6.95,6.93,3893,2701065.00,6.941",
                "2021-02-24 11:23,6.95,6.93,6.95,6.93,4004,2778748.00,6.941",
                "2021-02-24 11:24,6.93,6.92,6.93,6.91,2128,1472860.00,6.941",
                "2021-02-24 11:25,6.92,6.89,6.92,6.89,6840,4720370.00,6.941",
                "2021-02-24 11:26,6.89,6.90,6.91,6.89,2721,1876350.00,6.941",
                "2021-02-24 11:27,6.90,6.91,6.91,6.89,3667,2529245.00,6.941",
                "2021-02-24 11:28,6.90,6.90,6.91,6.89,2116,1459561.00,6.941",
                "2021-02-24 11:29,6.90,6.89,6.90,6.89,3397,2341454.00,6.941",
                "2021-02-24 11:30,6.89,6.88,6.89,6.88,5868,4039028.00,6.941",
                "2021-02-24 13:01,6.88,6.86,6.88,6.86,7595,5222135.00,6.941",
                "2021-02-24 13:02,6.87,6.88,6.88,6.86,3653,2508501.00,6.941",
                "2021-02-24 13:03,6.88,6.88,6.88,6.87,2471,1698711.00,6.940",
                "2021-02-24 13:04,6.88,6.87,6.88,6.87,1838,1263397.00,6.940",
                "2021-02-24 13:05,6.87,6.88,6.88,6.86,2200,1511979.00,6.940",
                "2021-02-24 13:06,6.88,6.87,6.88,6.87,6886,4725080.00,6.940",
                "2021-02-24 13:07,6.87,6.84,6.87,6.84,3207,2199663.00,6.940",
                "2021-02-24 13:08,6.85,6.80,6.85,6.80,7441,5075868.00,6.939",
                "2021-02-24 13:09,6.81,6.82,6.82,6.80,7311,4976126.00,6.939",
                "2021-02-24 13:10,6.82,6.84,6.84,6.82,2686,1834232.00,6.939",
                "2021-02-24 13:11,6.83,6.80,6.83,6.80,6828,4652054.00,6.938",
                "2021-02-24 13:12,6.80,6.77,6.80,6.76,17806,12080311.00,6.937",
                "2021-02-24 13:13,6.75,6.76,6.76,6.74,17233,11631668.00,6.936",
                "2021-02-24 13:14,6.75,6.73,6.76,6.73,8139,5487881.00,6.935",
                "2021-02-24 13:15,6.74,6.80,6.80,6.73,9430,6366562.00,6.934",
                "2021-02-24 13:16,6.80,6.81,6.82,6.80,3965,2699326.00,6.934",
                "2021-02-24 13:17,6.82,6.87,6.87,6.82,2799,1914112.00,6.934",
                "2021-02-24 13:18,6.87,6.86,6.89,6.85,7678,5272781.00,6.933",
                "2021-02-24 13:19,6.85,6.88,6.89,6.85,3622,2491135.00,6.933",
                "2021-02-24 13:20,6.89,6.90,6.90,6.89,5155,3554534.00,6.933",
                "2021-02-24 13:21,6.89,6.87,6.89,6.86,4376,3012406.00,6.933",
                "2021-02-24 13:22,6.87,6.86,6.87,6.85,1868,1281691.00,6.933",
                "2021-02-24 13:23,6.85,6.85,6.86,6.85,1541,1056664.00,6.933",
                "2021-02-24 13:24,6.85,6.85,6.86,6.85,3087,2115308.00,6.933",
                "2021-02-24 13:25,6.86,6.87,6.87,6.85,2289,1570670.00,6.933",
                "2021-02-24 13:26,6.86,6.84,6.87,6.84,2740,1878362.00,6.933",
                "2021-02-24 13:27,6.84,6.86,6.86,6.83,2769,1895102.00,6.933",
                "2021-02-24 13:28,6.85,6.85,6.87,6.84,4025,2760212.00,6.933",
                "2021-02-24 13:29,6.85,6.86,6.86,6.84,2131,1459007.00,6.932",
                "2021-02-24 13:30,6.85,6.87,6.88,6.85,1732,1188477.00,6.932",
                "2021-02-24 13:31,6.88,6.87,6.88,6.87,7955,5467015.00,6.932",
                "2021-02-24 13:32,6.87,6.85,6.87,6.85,3469,2377684.00,6.932",
                "2021-02-24 13:33,6.84,6.85,6.85,6.84,2829,1937134.00,6.932",
                "2021-02-24 13:34,6.85,6.84,6.85,6.84,1851,1266876.00,6.932",
                "2021-02-24 13:35,6.85,6.86,6.86,6.85,1636,1120783.00,6.932",
                "2021-02-24 13:36,6.86,6.85,6.87,6.85,3233,2218814.00,6.932",
                "2021-02-24 13:37,6.86,6.87,6.87,6.85,1648,1131355.00,6.932",
                "2021-02-24 13:38,6.87,6.84,6.87,6.84,3225,2211208.00,6.932",
                "2021-02-24 13:39,6.86,6.84,6.86,6.84,2470,1690405.00,6.931",
                "2021-02-24 13:40,6.85,6.84,6.85,6.84,927,634573.00,6.931",
                "2021-02-24 13:41,6.86,6.86,6.87,6.85,2313,1585081.00,6.931",
                "2021-02-24 13:42,6.86,6.86,6.87,6.85,2352,1612644.00,6.931",
                "2021-02-24 13:43,6.86,6.85,6.86,6.85,2043,1400638.00,6.931",
                "2021-02-24 13:44,6.85,6.84,6.86,6.84,2235,1530842.00,6.931",
                "2021-02-24 13:45,6.84,6.85,6.86,6.84,1601,1097008.00,6.931",
                "2021-02-24 13:46,6.85,6.84,6.85,6.84,2410,1649500.00,6.931",
                "2021-02-24 13:47,6.85,6.85,6.86,6.84,2553,1748606.00,6.931",
                "2021-02-24 13:48,6.85,6.87,6.87,6.85,3229,2214520.00,6.931",
                "2021-02-24 13:49,6.86,6.85,6.86,6.85,2249,1542046.00,6.931",
                "2021-02-24 13:50,6.85,6.84,6.86,6.83,2628,1798661.00,6.931",
                "2021-02-24 13:51,6.84,6.83,6.84,6.83,3006,2054207.00,6.930",
                "2021-02-24 13:52,6.83,6.82,6.83,6.82,3665,2501790.00,6.930",
                "2021-02-24 13:53,6.82,6.82,6.83,6.81,2493,1699627.00,6.930",
                "2021-02-24 13:54,6.83,6.82,6.83,6.81,2386,1626171.00,6.930",
                "2021-02-24 13:55,6.83,6.83,6.84,6.82,2357,1609058.00,6.930",
                "2021-02-24 13:56,6.83,6.82,6.83,6.81,2386,1626857.00,6.930",
                "2021-02-24 13:57,6.82,6.81,6.82,6.81,1983,1351098.00,6.930",
                "2021-02-24 13:58,6.82,6.78,6.82,6.77,12595,8558022.00,6.929",
                "2021-02-24 13:59,6.77,6.77,6.78,6.76,5476,3706891.00,6.929",
                "2021-02-24 14:00,6.78,6.81,6.81,6.78,3976,2703195.00,6.928",
                "2021-02-24 14:01,6.81,6.77,6.81,6.77,8070,5473695.00,6.928",
                "2021-02-24 14:02,6.78,6.77,6.78,6.76,8306,5621968.00,6.927",
                "2021-02-24 14:03,6.77,6.76,6.78,6.76,4358,2949070.00,6.927",
                "2021-02-24 14:04,6.77,6.74,6.77,6.74,8921,6026032.00,6.926",
                "2021-02-24 14:05,6.75,6.73,6.75,6.73,11068,7454706.00,6.925",
                "2021-02-24 14:06,6.73,6.75,6.75,6.73,4803,3236654.00,6.925",
                "2021-02-24 14:07,6.75,6.76,6.77,6.75,4515,3051835.00,6.925",
                "2021-02-24 14:08,6.76,6.77,6.77,6.75,4985,3371609.00,6.924",
                "2021-02-24 14:09,6.77,6.73,6.77,6.73,8480,5722220.00,6.924",
                "2021-02-24 14:10,6.75,6.72,6.75,6.72,6117,4116777.00,6.923",
                "2021-02-24 14:11,6.74,6.74,6.74,6.72,6614,4450040.00,6.923",
                "2021-02-24 14:12,6.74,6.74,6.74,6.73,3683,2481426.00,6.922",
                "2021-02-24 14:13,6.73,6.73,6.74,6.72,6137,4130112.00,6.922",
                "2021-02-24 14:14,6.73,6.74,6.74,6.73,6469,4355498.00,6.921",
                "2021-02-24 14:15,6.74,6.75,6.75,6.72,5994,4035408.00,6.921",
                "2021-02-24 14:16,6.76,6.77,6.77,6.76,6518,4407701.00,6.920",
                "2021-02-24 14:17,6.77,6.74,6.77,6.74,6577,4441888.00,6.920",
                "2021-02-24 14:18,6.73,6.76,6.76,6.73,2662,1795435.00,6.920",
                "2021-02-24 14:19,6.76,6.78,6.78,6.76,7579,5130601.00,6.919",
                "2021-02-24 14:20,6.78,6.83,6.83,6.78,6516,4432570.00,6.919",
                "2021-02-24 14:21,6.83,6.84,6.84,6.83,7460,5099278.00,6.919",
                "2021-02-24 14:22,6.84,6.82,6.84,6.82,4310,2945615.00,6.919",
                "2021-02-24 14:23,6.83,6.82,6.83,6.81,3342,2278742.00,6.918",
                "2021-02-24 14:24,6.81,6.81,6.83,6.81,2998,2043594.00,6.918",
                "2021-02-24 14:25,6.81,6.83,6.83,6.80,2737,1864799.00,6.918",
                "2021-02-24 14:26,6.82,6.82,6.83,6.81,3094,2110627.00,6.918",
                "2021-02-24 14:27,6.81,6.81,6.82,6.81,1828,1245660.00,6.918",
                "2021-02-24 14:28,6.81,6.79,6.82,6.78,4981,3385930.00,6.918",
                "2021-02-24 14:29,6.78,6.79,6.79,6.77,1870,1268141.00,6.918",
                "2021-02-24 14:30,6.79,6.79,6.79,6.77,4743,3216513.00,6.917",
                "2021-02-24 14:31,6.79,6.82,6.82,6.79,2860,1946465.00,6.917",
                "2021-02-24 14:32,6.82,6.83,6.83,6.81,4265,2907749.00,6.917",
                "2021-02-24 14:33,6.83,6.85,6.85,6.83,5515,3772437.00,6.917",
                "2021-02-24 14:34,6.85,6.82,6.85,6.82,14597,9982730.00,6.916",
                "2021-02-24 14:35,6.82,6.83,6.83,6.82,2940,2006925.00,6.916",
                "2021-02-24 14:36,6.82,6.83,6.83,6.82,2367,1615908.00,6.916",
                "2021-02-24 14:37,6.83,6.84,6.84,6.82,3416,2334179.00,6.916",
                "2021-02-24 14:38,6.84,6.85,6.85,6.83,5748,3931399.00,6.916",
                "2021-02-24 14:39,6.85,6.86,6.87,6.85,9389,6439072.00,6.916",
                "2021-02-24 14:40,6.86,6.88,6.88,6.86,13108,9015054.00,6.916",
                "2021-02-24 14:41,6.89,6.89,6.90,6.88,13839,9539476.00,6.915",
                "2021-02-24 14:42,6.89,6.88,6.90,6.88,11001,7578242.00,6.915",
                "2021-02-24 14:43,6.87,6.86,6.87,6.86,4780,3283119.00,6.915",
                "2021-02-24 14:44,6.87,6.87,6.88,6.86,2846,1953749.00,6.915",
                "2021-02-24 14:45,6.87,6.86,6.87,6.86,3934,2700634.00,6.915",
                "2021-02-24 14:46,6.87,6.85,6.87,6.84,6833,4683980.00,6.915",
                "2021-02-24 14:47,6.85,6.84,6.85,6.84,4434,3033232.00,6.915",
                "2021-02-24 14:48,6.84,6.85,6.85,6.83,2752,1882548.00,6.915",
                "2021-02-24 14:49,6.84,6.85,6.85,6.84,7676,5255089.00,6.915",
                "2021-02-24 14:50,6.85,6.85,6.85,6.84,4058,2778423.00,6.914",
                "2021-02-24 14:51,6.84,6.83,6.84,6.82,11008,7520137.00,6.914",
                "2021-02-24 14:52,6.82,6.82,6.84,6.82,9943,6787377.00,6.914",
                "2021-02-24 14:53,6.82,6.83,6.83,6.82,4702,3209315.00,6.914",
                "2021-02-24 14:54,6.83,6.81,6.84,6.81,14248,9718517.00,6.913",
                "2021-02-24 14:55,6.80,6.80,6.81,6.79,14368,9770692.00,6.912",
                "2021-02-24 14:56,6.80,6.79,6.80,6.78,11470,7792576.00,6.912",
                "2021-02-24 14:57,6.79,6.83,6.83,6.79,11960,8146681.00,6.911",
                "2021-02-24 14:58,6.83,6.83,6.83,6.83,542,370237.00,6.911",
                "2021-02-24 14:59,6.83,6.83,6.83,6.83,0,0.00,6.911",
                "2021-02-24 15:00,6.83,6.83,6.83,6.83,23520,16064419.00,6.911"]
shoupan20210223 = 6.89
turn_input_to_liuyao(data20210224, shoupan20210223)
