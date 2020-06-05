import math, ephem, datetime

yuefen = ["正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
nlrq = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八",
        "十九", "二十", "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
gz = [''] * 60  # 六十甲子表
for i in range(60):
    gz[i] = tiangan[i % 10] + dizhi[i % 12]


def EquinoxSolsticeJD(year, angle):
    if 0 <= angle < 90:
        date = ephem.next_vernal_equinox(year)  # 春分
    elif 90 <= angle < 180:
        date = ephem.next_summer_solstice(year)  # 夏至
    elif 180 <= angle < 270:
        date = ephem.next_autumn_equinox(year)  # 秋分
    else:
        date = ephem.next_winter_solstice(year)  # 冬至
    JD = ephem.julian_date(date)
    return JD


# 计算二十四节气
def SolarLongitube(JD):
    date = ephem.Date(JD - 2415020)
    s = ephem.Sun(date)  # date应为UT时间
    sa = ephem.Equatorial(s.ra, s.dec, epoch=date)
    se = ephem.Ecliptic(sa)
    L = se.lon / ephem.degree / 180 * math.pi
    return L


def SolarTerms(year, angle):
    if angle > 270: year -= 1  # 岁首冬至
    if year == 0: year -= 1  # 公元0改为公元前1
    JD = EquinoxSolsticeJD(str(year), angle)  # 初值
    if angle >= 270:
        JD0 = EquinoxSolsticeJD(str(year), (angle - 90) % 360)
        if JD < JD0:  # 非年末冬至
            JD = EquinoxSolsticeJD(str(year + 1), angle)  # 转入次年
    JD1 = JD
    while True:
        JD2 = JD1
        L = SolarLongitube(JD2)
        JD1 += math.sin(angle * math.pi / 180 - L) / math.pi * 180
        if abs(JD1 - JD2) < 0.00001:
            break  # 精度小于1 second
    return JD1  # UT


def EvenTerms(year, angle):  # 十二节
    if 225 <= angle <= 270: year -= 1  # 岁首冬至改为立冬
    JD = SolarTerms(year, angle)
    return JD


def DateCompare(JD1, JD2):  # 输入ut，返回ut+8的比较结果
    JD1 += 0.5 + 8 / 24
    JD2 += 0.5 + 8 / 24
    if math.floor(JD1) >= math.floor(JD2):
        return True
    else:
        return False


def dzs_search(year):  # 寻找年前冬至月朔日
    if year == 1: year -= 1  # 公元0改为公元前1
    dz = ephem.next_solstice((year - 1, 12))  # 年前冬至
    jd = ephem.julian_date(dz)
    # 可能的三种朔日
    date1 = ephem.next_new_moon(ephem.Date(jd - 2415020 - 0))
    jd1 = ephem.julian_date(date1)
    date2 = ephem.next_new_moon(ephem.Date(jd - 2415020 - 29))
    jd2 = ephem.julian_date(date2)
    date3 = ephem.next_new_moon(ephem.Date(jd - 2415020 - 31))
    jd3 = ephem.julian_date(date3)
    if DateCompare(jd, jd1):  # 冬至合朔在同一日或下月
        return date1
    elif DateCompare(jd, jd2) and (not DateCompare(jd, jd1)):
        return date2
    elif DateCompare(jd, jd3):  # 冬至在上月
        return date3


def Solar2LunarCalendar(date):  # 默认输入ut+8时间
    JD = ephem.julian_date(date) - 8 / 24  # ut
    year = ephem.Date(JD + 8 / 24 - 2415020).triple()[0]
    d: ephem.Date = ephem.Date(JD + 8 / 24 - 2415020)
    d.tuple()
    shuo = []  # 存储date
    shuoJD = []  # 存储JD
    # 判断所在年
    shuo.append(dzs_search(year))  # 本年冬至朔
    next_dzs = dzs_search(year + 1)  # 次年冬至朔
    this_dzsJD = ephem.julian_date(shuo[0])
    next_dzsJD = ephem.julian_date(next_dzs)
    nian = year  # 农历年
    if DateCompare(JD, next_dzsJD):  # 该日在次年
        shuo[0] = next_dzs  # 次年冬至朔变为本年
        next_dzs = dzs_search(year + 2)
        nian += 1
    if not DateCompare(JD, this_dzsJD):  # 该日在上年
        next_dzs = shuo[0]  # 本年冬至朔变为次年
        shuo[0] = dzs_search(year - 1)
        nian -= 1
    next_dzsJD = ephem.julian_date(next_dzs)
    shuoJD.append(ephem.julian_date(shuo[0]))  # 找到的年前冬至朔
    # 查找所在月及判断置闰
    run = ''
    szy = 0
    i = -1  # 中气序，从0起计
    j = -1  # 计算连续两个冬至月中的合朔次数，从0起计
    zry = 99  # 无效值
    flag = False
    while not DateCompare(shuoJD[j + 1], next_dzsJD):  # 从冬至月起查找，截止到次年冬至朔
        i += 1
        j += 1
        # 查找所在月，起冬至朔
        if DateCompare(JD, shuoJD[j]):
            szy += 1  # date所在月
            newmoon = shuoJD[j]
        shuo.append(ephem.next_new_moon(shuo[j]))  # 次月朔
        shuoJD.append(ephem.julian_date(shuo[j + 1]))
        # 查找本月中气，若无则置闰
        if j == 0: continue  # 冬至月一定含中气，从次月开始查找
        angle = (-90 + 30 * i) % 360  # 本月应含中气，起冬至
        qJD = SolarTerms(nian, angle)
        # 不判断气在上月而后气在后月的情况，该月起的合朔次数不超过气数，可省去
        if DateCompare(qJD, shuoJD[j + 1]) and flag == False:  # 中气在次月，则本月无中气
            zry = j + 1  # 置闰月
            i -= 1
            flag = True  # 仅第一个无中气月置闰
    # 判断置闰
    if j == 11 and zry != 99:  # 有无中气月但合朔仅12次
        zry = 99
    if szy % 12 == zry % 12 and zry != 99:
        run = '闰'
    if szy >= zry % 12 and zry != 99:
        szy -= 1  # 置闰后的月序名
    # 以正月开始的年干支
    if szy < 3: nian -= 1  # 正月前属上年
    if nian < 0: nian += 1
    rq = math.floor(JD + 8 / 24 + 0.5) - math.floor(newmoon + 8 / 24 + 0.5)  # 日干支
    # 判断节气月，起年首前大雪
    lidong = EvenTerms(year, 225)  # 岁首前立冬
    k = int((JD - lidong) // 30)  # 平气法
    jJD1 = EvenTerms(year + (k + 1) // 12, (225 + (k + 1) * 30) % 360)
    jJD2 = EvenTerms(year + k // 12, (225 + k * 30) % 360)
    if DateCompare(JD, jJD1):
        jqx = k
    elif not DateCompare(JD, jJD2):
        jqx = k - 2
    else:
        jqx = k - 1  # jJD2 ≤ JD < jJD1
    if year < 0: year += 1
    jqy = gz[(year * 12 + 12 + jqx) % 60]
    nian_jia_zi = gz[(nian - 4) % 60]
    yue_jia_zi = jqy
    ri_jia_zi = gz[math.floor(JD + 8 / 24 + 0.5 + 49) % 60]
    nongli_ri = run + yuefen[(szy - 3) % 12] + nlrq[rq]
    return nian_jia_zi, yue_jia_zi, ri_jia_zi, nongli_ri


def Lunar2SolarCalendar(nian, date):  # 正月开始的年
    date1 = date.split('闰')[-1]
    yx = yuefen.index(date1.split('月')[0] + '月')
    year = nian
    if yx + 1 > 10: year += 1  # 计算用年，起冬至朔
    yx = (yx + 2) % 12
    if '闰' in date:
        yx += 1
        leap = True
    else:
        leap = False
    shuo = []  # 存储date
    shuoJD = []  # 存储JD
    shuo.append(dzs_search(year))  # 本年冬至朔
    shuoJD.append(ephem.julian_date(shuo[0]))
    next_dzsJD = ephem.julian_date(dzs_search(year + 1))
    # 查找所在月及判断置闰
    i = -1  # 中气序
    j = -1  # 计算连续两个冬至月中的合朔次数
    flag = False
    while not DateCompare(shuoJD[j], next_dzsJD):  # 从冬至月起查找，截止到次年冬至朔
        i += 1
        j += 1
        shuo.append(ephem.next_new_moon(shuo[j]))  # 次月朔
        shuoJD.append(ephem.julian_date(shuo[j + 1]))
        # 查找本月中气，若无则置闰
        if j == 0:
            qJD = SolarTerms(year - 1, 270)  # 起冬至
        else:
            angle = (-90 + 30 * i) % 360
            qJD = SolarTerms(year, angle)  # 该月应含中气
        if DateCompare(qJD, shuoJD[j + 1]) and flag == False:  # 中气在次月，则该月为闰月
            i -= 1
            if leap == False: yx += 1  # 该月前有闰
            flag = True  # 仅第一个无中气月置闰
        if yx == j: k = yx  # 所在月
    if j == 12 and flag == True: k -= 1
    try:
        rq = nlrq.index(date.split('月')[1])
    except:
        rgz = gz.index(date.split('月')[1])
        sgz = math.floor(shuoJD[k] + 8 / 24 + 0.5 + 49) % 60
        rq = (rgz - sgz) % 60
        if DateCompare(shuoJD[k] + rq, shuoJD[k + 1]):
            print('该月无' + date.split('月')[1])
        else:
            print(date.split('月')[1] + '为该月' + nlrq[rq] + '日')
    date2 = str(ephem.Date(shuoJD[k] + rq + 8 / 24 - 2415020))[:-9]
    return '农历' + str(nian) + '年' + date + ' 为公历：' + date2


tropicl_year = 365.24219647  # 回归年长度
# 24节气，偶数为气，奇数为节
jieqi = ["春分", "清明", "谷雨", "立夏", "小满", "芒种", \
         "夏至", "小暑", "大暑", "立秋", "处暑", "白露", \
         "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", \
         "冬至", "小寒", "大寒", "立春", "雨水", "惊蛰"]


# 计算黄经
def ecliptic_lon(jd_utc):
    s = ephem.Sun(jd_utc)  # 构造太阳
    equ = ephem.Equatorial(s.ra, s.dec, epoch=jd_utc)  # 求太阳的视赤经视赤纬（epoch设为所求时间就是视赤经视赤纬）
    e = ephem.Ecliptic(equ)  # 赤经赤纬转到黄经黄纬
    return e.lon  # 返回黄纬


def iteration(n, jd_utc):  # 迭代求时间
    while True:
        e = ecliptic_lon(jd_utc)
        dd = (n * 15 - e * 180.0 / math.pi) / 360 * tropicl_year  # 24节气对应的太阳黄经和当前时间求得的太阳黄经差值转为天数
        if dd > 360:  # 春分时太阳黄经为0，dd有可能差值过大
            dd -= tropicl_year
        jd_utc += dd
        if abs(dd) < 0.000000001:  # 0.0864秒
            break
    d = ephem.Date(jd_utc + 1 / 3)
    d = d.tuple()
    if n == 24:  # 春分时n=24
        n -= 24
    r_str = "{0}-{1:02d}-{2:02d} {3}：{4:02d}:{5:02d}:{6:03.1f}" \
        .format(d[0], d[1], d[2], jieqi[n], d[3], d[4], d[5])
    date = datetime.datetime(d[0], d[1], d[2], d[3], d[4], math.floor(d[5]))
    jie_qi_str = jieqi[n]
    return jie_qi_str, date, r_str, n


def jq(date_str=ephem.now(), num=1):  # 从当前时间开始连续输出未来n个节气的时间
    jd_utc = ephem.Date(date_str)  # 获取当前时间的一个儒略日和1899/12/31 12:00:00儒略日的差值
    e = ecliptic_lon(jd_utc)
    n = math.ceil(e * 180.0 / math.pi / 15)
    results = []
    for i in range(num):
        if n > 24:
            n -= 24
        results.append(iteration(n, jd_utc))
        jd_utc += 15
        n += 1
    if num == 1:
        return results[0]
    else:
        return results


def get_jie_or_qi(elements, jie=True, first=True):
    """
    从几个节气中，找到节或者气。
    :param elements:所有的节气元素
    :param jie:是节还是气
    :param first:是否返回第一个节或者气，如果不返回第一个，那么就返回最后一个
    :return:
    """
    result = None
    for r_jie_qi in elements:
        jie_qi_index = jieqi.index(r_jie_qi[0])
        print(r_jie_qi[0])
        if (jie and jie_qi_index % 2 == 1) or ((not jie) and jie_qi_index % 2 == 0):
            print(r_jie_qi[0])
            result = r_jie_qi
            if first:
                break
            else:
                continue

    return result


def jie_before(date: datetime.datetime):
    result = []
    jie = select_jie(date, next=False)
    jq_result = list(jie)
    result += jq_result
    result.append(date - jq_result[1])
    return result


def jie_after(date: datetime.datetime):
    result = []
    jq_result = select_jie(date, next=True)
    result += jq_result
    result.append(jq_result[1] - date)
    return result


def get_jie_of_year(year: int):
    date_str = datetime.datetime(year - 1, 11, 1, 0, 0, 0).strftime("%Y/%m/%d %H:%M:%S")
    jqs = jq(date_str, 28)
    results = []
    for e in jqs:
        name = e[0]
        index = jieqi.index(name)
        if index % 2 == 1:
            results.append(e)
    return results


# rs = get_jie_of_year(2020)
# for r in rs:
#     print(r)


def select_jie(date: datetime.datetime, next=True):
    year = date.year
    year_jies = get_jie_of_year(year)
    result = None
    for jie in year_jies:
        jie_date = jie[1]
        print(jie)
        if next:
            if jie_date > date:
                result = jie
                break
        else:
            if jie_date < date:
                result = jie
            else:
                break
    return result


class Calendar:
    def get_lunar_info(self, date):
        pass

    pass

# results = jq(num=24)
# for r in results:
#     print(r)
