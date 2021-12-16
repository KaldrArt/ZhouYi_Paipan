from datetime import datetime
from common.output import liuyao_gua_output_path
from common.utils import mkdir

example = """
李洪成六爻在线摇卦
www.zhouyi.com.cn/paipan
求测人年龄:32 性别:女
预测策项:项目前景
起卦钥语:我从事基因与轻食配餐项目是否有好的收益？
前提条件:还在筹划调研阶段
起卦时间:2021年4月8日未时
壬辰月 丙戌日(午未空)531234卦
  《家 人》 《天水讼》 六神
   兄卯、    戌、  龙
   孙巳、 应  申、  玄
   才未×    午、  虎
官酉：父亥○    午..  蛇
   才丑× 巽  辰、  勾
   兄卯○    寅..  雀
"""


def array_to_markdown_table(table_titles, lines=[]):
    result = ""
    line = "|" + "|".join(table_titles) + "|"
    result += line + "\n"
    cell_align = "|"
    for i in range(0, len(table_titles)):
        cell_align += ":-|"
    result += cell_align + "\n"
    for line in lines:
        content = "|"
        for cell in line:
            content += str(cell) + "|"
        result += content + "\n"
    return result


class DaZongYiTransformer:
    titles = ["伏神", '本卦', "阴阳", "应世", "变卦", "阴阳", "六神"]
    tiangan = "甲乙丙丁戊己庚辛壬癸"
    liuqin = "兄孙才财官父"
    liushen = "玄蛇雀龙勾虎"
    dizhi = "子丑寅卯辰巳午未申酉戌亥"
    bagua = "乾兑离震巽坎艮坤"
    output_path = liuyao_gua_output_path

    def __init__(self, text, detailed=False, print=False, save=False):
        self.text = text
        self.gua = []
        self.info = {
            "age": 0,
            "gender": "男",
            "profession": "",
            "project": "杂占",
            "content": "",
            "condition": "",
            "time": "",
            "event_time": "",
            "code": "",
            "timelimit": "",
            'method': ""
        }
        self.print = print
        self.content = []
        self.is_jing = False
        self.info_mk_table = ""
        self.detailed_mk_table = ""
        self.mk_table = ""
        self.split_content()
        self.get_info()
        self.transfer_text_to_markdown()
        self.simple_info_to_markdown()
        self.detailed = detailed

        print_info = self.print_info()
        if save:
            self.save_file(print_info)

    def save_file(self, info):
        folder = self.output_path + self.info['project'] + "/"
        mkdir(folder)
        filename = folder + self.info['content'][0:10] + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".md"
        with open(filename, 'w') as f:
            f.write(info)
            f.close()

    def print_info(self):
        h11 = "# 一、求测内容"
        c11 = self.info_mk_table
        h12 = "# 二、卦"
        c12 = self.mk_table
        c13 = ""
        if self.detailed:
            c13 = self.detailed_mk_table
        h13 = "# 三、断语"
        c14 = ""
        h14 = "# 四、实际情况"
        content = [h11, c11, h12, c12, c13, h13, c14, h14]
        if self.print:
            for c in content:
                print(c)
        return '\n'.join(content)

    def split_content(self):
        self.text = self.text.replace("\u3000", "").replace(" ", "").replace("\t", "")
        self.content = self.text.split("\n")

    def get_info(self):
        start_gua = False
        for line in self.content:
            if line.startswith("====") or line.startswith("小成图"):
                break
            if not start_gua:
                if line.startswith("求测人年龄"):
                    strs = line.split(":")
                    self.info['gender'] = strs[2][0]
                    self.info['age'] = strs[1].replace("性别", "")
                    self.info['profession'] = ""
                    if len(strs) > 3:
                        self.info['profession'] = strs[3]
                elif line.startswith("预测策项"):
                    self.info['project'] = line.split(":")[1]
                elif line.startswith("起卦钥语") or line.startswith("求测内容"):
                    self.info['content'] = line.split(":")[1]
                elif line.startswith("前提条件"):
                    self.info['condition'] = line.split(":")[1]
                elif line.startswith("策项时限"):
                    self.info['timelimit'] = line.split(":")[1]
                elif line.startswith("起卦时间"):
                    self.info['time'] = line.split(":")[1]
                elif line.startswith("事项时间"):
                    self.info['event_time'] = line.split(":")[1]
                elif line.startswith("起卦方式"):
                    self.info['method'] = line.split(":")[1]
                elif line.startswith("排盘"):
                    start_gua = True
            else:
                self.gua.append(line)

    def simple_info_to_markdown(self):
        mk_titles = ["项目", '内容']
        mk_lines = [
            ["年龄", self.info['age']],
            ["职业", self.info['profession']],
            ['性别', self.info['gender']],
            ['策项', self.info['project']],
            ['钥语', self.info['content']],
            ['条件', self.info['condition']],
            ['时限', self.info['timelimit']],
            ['起卦时间', self.info['time']],
            ['事件时间', self.info['event_time']],
            ['起卦方式', self.info['method']],
            ['卦码', self.info['code']],

        ]
        self.info_mk_table = array_to_markdown_table(mk_titles, mk_lines)

    def gua_to_markdown(self):
        ri_yue = []
        gua_name = []
        result = []
        simple_result = []
        for line in self.gua:
            if not line:
                continue
            if line[0] in self.tiangan:
                ri_yue = self.get_ri_yue(line)
            elif line[0] == "《":
                gua_count = 0
                for char in line:
                    if char == "《":
                        gua_count += 1
                if gua_count == 1:
                    self.is_jing = True
                gua_name = self.get_gua_name(line)
            else:
                yao = self.get_yao(line)
                result.append(yao)
                simple_result.append([yao[0], yao[1] + yao[2] + yao[3], yao[4] + yao[5], yao[6]])

        titles = ["", gua_name[1], ri_yue[1], ri_yue[4], gua_name[4], ri_yue[5], ri_yue[6]]
        simple_titles = ["**%s**" % '伏神',
                         "**%s**" % gua_name[1],
                         "**%s**" % gua_name[4],
                         "**%s**" % '六神']
        simple_result.insert(0, simple_titles)

        self.detailed_mk_table = array_to_markdown_table(titles, result)
        self.mk_table = array_to_markdown_table(['', ri_yue[1], ri_yue[4], ri_yue[5]], simple_result)

    def get_yao(self, line):
        line = line.replace(":", "").replace("：", "")
        result = ["", "", "", "", "", "", ""]
        dizhi_count = 0
        for s in line:
            if s in self.dizhi:
                dizhi_count += 1
        if (dizhi_count == 3 and not self.is_jing) or (self.is_jing and dizhi_count == 2):
            fu_shen = line[0:2]
            other = line[2:]
            result = self.get_yao(other)
            result[0] = fu_shen
        else:
            result[6] = line[-1]
            if "应" in line:
                line = line.replace("应", "")
                result[3] = "应"
            else:
                for s in self.bagua:
                    if s in line:
                        result[3] = s
                        line = line.replace(s, "")
                        break
            result[1] = line[0:2]
            if not self.is_jing:
                if line[-2] == ".":
                    result[5] = ".."
                elif line[-2] == "、":
                    result[5] = "、"
            if line[2] == ".":
                result[2] = ".."
            elif line[2] == "、":
                result[2] = "、"
            elif line[2] == "○":
                result[2] = "○"
            elif line[2] == "×":
                result[2] = "×"
            line = line.replace(".", "").replace("×", "").replace("、", "").replace("○", "")
            if not self.is_jing:
                result[4] = line[2]
        return result

    def get_gua_name(self, line):
        strs = line.replace("《", "").split("》")
        if self.is_jing:
            return ["", "%s" % strs[0], "", "", "", "", ""]
        else:
            return ["", "%s" % strs[0], "", "", "%s" % strs[1], "", ""]

    def get_ri_yue(self, line):
        code = line.split(")")[1]
        result = ['',
                  "%s" % line.split('月')[0] + "月",
                  '',
                  '',
                  "%s" % line.split("日")[0].split("月")[1] + "日",
                  line.split("空")[0].split("(")[1] + "空",
                  code
                  ]
        self.info['code'] = code
        return result

    def transfer_text_to_markdown(self):
        self.gua_to_markdown()

# DaZongYiTransformer(example, print=True)
