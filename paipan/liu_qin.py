from enum import Enum
from common import *
from paipan.pai_pan import PaiPan
import prettytable as pt
import sys

liu_qin_list = ["偏印", "正印",
                "偏官", "正官",
                "食神", "伤官",
                "偏财", "正财",
                "比肩", "劫财"]


class LiuQin:
    def __init__(self, base_gan: TianGanBase, effect_gan: TianGanBase):
        self.base_gan = base_gan
        self.effect_gan = effect_gan
        self.yong_shen = False
        self.tou = False
        self.jia_zi = None
        self.position_name = ""
        self.relation = effect_gan.shi_shen_relation[base_gan.name]
        self.position_id = -1

    def set_tou(self, tou=False):
        self.tou = tou

    def set_yong_shen(self, yong_shen=False):
        self.yong_shen = yong_shen

    def set_position_name(self, name):
        self.position_name = name
        if name == "年柱":
            self.position_id = 0
        elif name == "月柱":
            self.position_id = 1
        elif name == '日柱':
            self.position_id = 2
        elif name == "时柱":
            self.position_id = 3

    def set_jia_zi(self, jia_zi):
        self.jia_zi = jia_zi

    def __str__(self):
        return "%s(%s,%s,%s,%s)" % (
            self.relation.name,
            self.effect_gan.name, self.tou, self.jia_zi.name if self.jia_zi else False, self.position_name
        )


class LiuQinBasic:
    def __init__(self, pai_pan: PaiPan):
        self.pai_pan = pai_pan
        self.liu_qin: dict = self.generate_liu_qin()

    def __str__(self):
        tb = pt.PrettyTable(encoding=sys.stdout.encoding)
        tb.field_names = ['六亲', '天干', '透干', '地支']
        for liu_qin_name in self.liu_qin:
            liu_qin_ob = self.liu_qin[liu_qin_name]
            tb.add_row([liu_qin_name, liu_qin_ob.effect_gan.name, liu_qin_ob.position_name, ""])
        return tb.__str__()

    def generate_liu_qin(self):
        pai_pan_ba_zi_tian_gans = [
            self.pai_pan.nian_zhu.tian_gan.name,
            self.pai_pan.yue_zhu.tian_gan.name,
            self.pai_pan.ri_zhu.tian_gan.name,
            self.pai_pan.shi_zhu.tian_gan.name
        ]
        target_gan = self.pai_pan.ri_zhu.tian_gan.name
        tian_gans = [TianGan[x].value for x in tian_gan_list]
        result = {}
        for item in tian_gans:
            tian_gan_item: TianGanBase = item
            current_liu_qin = LiuQin(self.pai_pan.ri_zhu.tian_gan, tian_gan_item)
            current_liu_qin.set_tou(tian_gan_item.name in pai_pan_ba_zi_tian_gans)
            if tian_gan_item.name == self.pai_pan.nian_zhu.tian_gan.name:
                current_liu_qin.set_jia_zi(self.pai_pan.nian_zhu)
                current_liu_qin.set_position_name("年柱")
            elif tian_gan_item.name == self.pai_pan.yue_zhu.tian_gan.name:
                current_liu_qin.set_jia_zi(self.pai_pan.yue_zhu)
                current_liu_qin.set_position_name("月柱")
            elif tian_gan_item.name == self.pai_pan.ri_zhu.tian_gan.name:
                current_liu_qin.set_jia_zi(self.pai_pan.ri_zhu)
                current_liu_qin.set_position_name("日柱")
            elif tian_gan_item.name == self.pai_pan.shi_zhu.tian_gan.name:
                current_liu_qin.set_jia_zi(self.pai_pan.shi_zhu)
                current_liu_qin.set_position_name("时柱")
            result[tian_gan_item.shi_shen_relation[target_gan].name] = current_liu_qin
        return result
