from common import *
from .pai_pan import PaiPan
import prettytable as pt
import sys
from .da_yun import DaYunDetail
from .liu_nian import LiuNian


class PaiPanPrinter:
    def __init__(self, pai_pan: PaiPan, print_liu_nian_year=False):
        self.pai_pan = pai_pan
        self.print_liu_nian_year = print_liu_nian_year
        self.print_all()

    def print_bazi(self):
        ri_zhu = self.pai_pan.ri_zhu.tian_gan.name
        tb = pt.PrettyTable(encoding=sys.stdout.encoding)
        titles = ['性别',
                  self.pai_pan.nian_zhu.tian_gan.shi_shen_relation[ri_zhu].name,
                  self.pai_pan.yue_zhu.tian_gan.shi_shen_relation[ri_zhu].name,
                  "日主",
                  self.pai_pan.shi_zhu.tian_gan.shi_shen_relation[ri_zhu].name,
                  "空亡",
                  "胎元"
                  ]
        t_u = set(titles)
        if not (len(t_u) == len(titles)):
            tb._validate_field_names = lambda *a, **k: None

        tb.field_names = titles
        tb.add_row(["乾造" if self.pai_pan.gender else "坤造",
                    self.pai_pan.nian_zhu.tian_gan.name,
                    self.pai_pan.yue_zhu.tian_gan.name,
                    self.pai_pan.ri_zhu.tian_gan.name,
                    self.pai_pan.shi_zhu.tian_gan.name,
                    "".join([x.name for x in self.pai_pan.kong_wang]),
                    ""
                    ])
        tb.add_row(["",
                    self.pai_pan.nian_zhu.di_zhi.name,
                    self.pai_pan.yue_zhu.di_zhi.name,
                    self.pai_pan.ri_zhu.di_zhi.name,
                    self.pai_pan.shi_zhu.di_zhi.name,
                    "", ""])
        tb.add_row([
            "",
            cang_gan[self.pai_pan.nian_zhu.di_zhi.name],
            cang_gan[self.pai_pan.yue_zhu.di_zhi.name],
            cang_gan[self.pai_pan.ri_zhu.di_zhi.name],
            cang_gan[self.pai_pan.shi_zhu.di_zhi.name],
            "",
            self.pai_pan.tai_yuan.name
        ])
        print(tb)

    def print_dayun(self):
        title = []
        content = []
        for j in range(10):
            c = []
            for i in range(2 * len(self.pai_pan.da_yun.da_yun_list)):
                c.append("")
            content.append(c)

        column = 0
        for item in self.pai_pan.da_yun.da_yun_list:
            dayun_item: DaYunDetail = item
            title.append(dayun_item.name)
            title.append(dayun_item.start_year)
            row = 0
            for inner_item in dayun_item.liu_nian_list:
                inner_liunian: LiuNian = inner_item
                content[row][column * 2 + 1] = "%s年%s岁" % (str(inner_liunian.year)[2:], inner_liunian.age)
                content[row][column * 2] = "%s" % inner_liunian.name
                row += 1
            column += 1
        tb = pt.PrettyTable(encoding=sys.stdout.encoding)
        tb.field_names = title
        for row in content:
            tb.add_row(row)
        print(tb)

    def print_dayun_simple(self):
        tb = pt.PrettyTable(encoding=sys.stdout.encoding)
        titles = []
        contents = [[], [], [], [], [], [], [], [], [], [], [], []]
        da_yun_index = 0
        for item in self.pai_pan.da_yun.da_yun_list:
            da_yun: DaYunDetail = item
            titles.append(da_yun.name)
            contents[0].append(da_yun.start_year)
            contents[11].append(da_yun.end_year)
            liu_nian_index = 1
            for inner_item in da_yun.liu_nian_list:
                liu_nian: LiuNian = inner_item
                contents[liu_nian_index].append(liu_nian.name)
                liu_nian_index += 1
            da_yun_index += 1
        tb.field_names = titles
        for row in contents:
            tb.add_row(row)
        print(tb)

    def print_xiaoyun(self):
        tb = pt.PrettyTable(encoding=sys.stdout.encoding)
        title = ["小运"]
        for i in range(len(self.pai_pan.xiao_yun_list)):
            title.append(self.pai_pan.date.year + i)
        tb.field_names = title
        content = [""]
        for xiaoyun in self.pai_pan.xiao_yun_list:
            content.append(xiaoyun.name)
        tb.add_row(content)
        print(tb)

    def print_basic_info(self):
        print("起运时间：%s" % self.pai_pan.qi_yun_time)

    def print_all(self):
        self.print_basic_info()
        self.print_bazi()
        if self.print_liu_nian_year:
            self.print_dayun()
        else:
            self.print_dayun_simple()
        self.print_xiaoyun()
