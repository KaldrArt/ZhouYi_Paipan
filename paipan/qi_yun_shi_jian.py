from datetime import datetime, timedelta, timezone
from common.calendar import jie_before, jie_after, tropicl_year

sh = timezone(timedelta(hours=8))
a = """
大运起运时间的计算方法，是以出生之日所在月令，按男女顺逆方法推算到下一个节或者上一个节，记下日数。然后按三天为一年，一天为四个月，一个时辰为十天来折算，加上出生时间就是起运的时间。

起运只论十二节不论十二气，阴年生女同阳年生男计算方法一致，阴年生男同阳年生女计算方法一致。

阳年男命和阴年女命的起运时间计算：

什么是起运时间，八字大运起始时间的计算

男女起运的时间计算方法不同，当确定了大运的顺逆之后，才可以计算起运的时间。阳年男命和明年女命都是顺行大运。从出生的月、日、时开始计算，顺数至最近的一个节的日、时，准确至小时，得出的数字。然后按三天为一年，一天为四个月，一个时辰为十天来折算，将结果加上出生时的时间，即为起运时间。

如某男一九九四年正月十七日寅时生，—九九四年为甲戌年阳年男命顺排，从出生到惊蛰节为八天，合为两年零八个月，起运时间：一九九六年九月十七日。

阴年男命和阳年女命的起运时间计算：

阴年男命和阳年女命都是逆行大运。从出生的时间开始倒数至上一个节的日时，得出的数字，按三天为一年，一天为四个月，一个时辰为十天来折算，将结果加上出生时的。

八字大运起始时间的计算
什么是起运时间，八字大运起始时间的计算

大运是八字预测的时间轴，离了了大运，八字预测的精确度必将大打折扣。

尽管现今我们能够直接排出八字之大运，本着知其然须知其所以然的学习态度，有必要了解八字预测中大运的起排方法。

一、方法说明：

1、大运的起排是以生辰八字中月柱的干支为基点。

2、大运起排的顺序是：阳年出生的男性、阴年出生的女性，大运是顺行排列;而阴年出生的男性、阳年出生的女性，则是逆行排列。阳年者，是指生辰八字中年柱天干为甲、丙、戊、庚、壬也;而阴年是指生辰八字中年柱天干为乙、丁、己、辛、癸也。大运顺行排列者，即将六十花甲按甲子、乙丑、丙寅、丁卯……庚申、辛酉、壬戌、癸亥之顺序排列也;而大运逆行排列者，即将六十花甲按癸亥、壬戌、辛酉、庚申……丁卯、丙寅、乙丑、甲子之顺序排列也。

3、大运起始时间点的计算。其分以下两种情况

什么是起运时间，八字大运起始时间的计算

一是阳年出生的男性、阴年出生的女性大运起始时间点的计算方法。从出生之日时算起，到出生之后的下一个节令为止。按三天计为一岁行大运，即一天计四个月行大运、一个时辰计十天行大运等之类。

二是阴年出生的男性、阳年出生的女性大运起始时间点的计算方法。从出生之日时算起，到出生之后的上一个节令为止。按三天计为一岁行大运，即一天计四个月行大运、一个时辰计十天行大运等之类。

方舟周易在此温馨提示：何为节令呢?节令即二十四节气中的每两个节气中的前面一个叫节、或节令，即立春、惊蛰、清明、立夏、芒种、小暑、立秋、白露、寒露、立冬、大雪、小寒十二个;而其余的十二个则叫气，合称节气。

4、大运是每十年更替一次的。
"""


class QiYunShiJian:
    def __init__(self, date: datetime, gender: bool, nian_gan_yin_yang: bool):
        self.birthday = date
        self.gender = gender
        self.info = ""
        self.nian_gan_yin_yang = nian_gan_yin_yang
        self.qi_yun_shi_jian = self.get_qi_yun_shi_jian()

    def get_qi_yun_shi_jian(self):
        self.info = "%s出生在%s年，大运" % (
            "男" if self.gender else "女",
            "阳" if self.nian_gan_yin_yang else "阴"
        )
        if self.nian_gan_yin_yang == self.gender:
            self.info += "顺排"
            jie_qi_info = self.get_next_jie()
            self.info += "出生后第一个节气是%s（%s）" % (jie_qi_info[0], jie_qi_info[1].strftime("%Y/%m/%d %H:%M:%S"))
        else:
            self.info += "逆排"
            jie_qi_info = self.get_previous_jie()
            self.info += "出生前第一个节气是%s（%s）" % (jie_qi_info[0], jie_qi_info[1].strftime("%Y/%m/%d %H:%M:%S"))
        self.info += "，"
        return self.get_time(jie_qi_info)

    def get_previous_jie(self):
        return jie_before(self.birthday)

    def get_next_jie(self):
        jq_info = jie_after(self.birthday)
        return jq_info

    def get_time(self, jie_qi_info):
        time_delta = jie_qi_info[4].total_seconds()
        if time_delta < 0:
            time_delta = -time_delta
        start_yun_time = self.birthday + timedelta(seconds=time_delta * tropicl_year / 3)

        self.info += "起运时间为%s" % start_yun_time
        return start_yun_time
