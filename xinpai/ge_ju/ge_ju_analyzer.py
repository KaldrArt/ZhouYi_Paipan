from paipan import *
from enum import Enum


class TianGanShengYuLingWangRuo(Enum):
    """
    天干生于令的旺弱
    """
    旺 = "旺"
    弱 = "弱"
    不旺不弱 = "不旺不弱"


class TianGanYuXiangLinGanZhiWangRuo(Enum):
    """
    天干于相邻干支的旺弱
    """
    旺 = "旺"
    弱 = "弱"


class GeJuAnalyzer:
    """
    格局分析
    一、日主在令的旺弱
    1.1 月令空亡
        生于年令，根据年令对日干的作用断旺衰
        1.1.1 旺
        1.1.2 弱
        1.1.3 不旺也不弱
            根据月干对日干的作用断旺衰
            TODO: 根据年干对日干的作用断旺衰，并且
    1.2 月令不空
        1.2.1 月令受制2次
            1.2.1.1 日支没有受制2次
                1.2.1.1.1 年支和日支对日主作用相同
                    根据作用来断旺衰，同旺则身旺，同弱则身弱
                1.2.1.1.2 年支和日支对日主的作用不同
                    根据1.2.2来断
            1.2.1.2 日支受制2次
                根据1.2.2来断
        1.2.2 月令没有受制2次
            生于月令，根据月令对日干的作用断旺衰
            1.2.2.1 旺
            1.2.2.2 弱
            1.2.2.3 不旺也不弱
                根据月干对日干的作用断旺衰

    二、检查在日支、月干、日干的旺弱，来判断是否是从格
    """

    def __init__(self, pai_pan_input: PaiPan, liu_qin_relation=LiuQinBasic):
        self.pai_pan = pai_pan_input
        self.liu_qin_relation = liu_qin_relation
        self.yue_ling_kong_wang = self.check_yue_ling_kong_wang()
        self.check_from_yue_gan = False
        self.ri_zhu_ling_wang_ruo = TianGanShengYuLingWangRuo.弱
        # 一、检查日柱在月令或者年令的旺弱
        if self.yue_ling_kong_wang:
            # 1.1 月令空亡
            self.ri_zhu_ling_wang_ruo = self.check_ri_zhu_yu_ling_you_li(from_ling='nian_ling')
        else:
            # 1.2 月令不空
            if self.check_ling_shou_zhi_twice('yue_ling'):
                # 1.2.1 月令受制2次
                if self.check_ling_shou_zhi_twice('ri_ling'):
                    # 1.2.1.2 日支受制2次
                    self.ri_zhu_ling_wang_ruo = self.check_ri_zhu_yu_ling_you_li(from_ling='yue_ling')
                else:
                    # 1.2.1.1 日支没有受制2次
                    ri_zhu_yu_nian_zhi_wang_ruo = self.check_ri_zhu_yu_ling_you_li(from_ling='nian_ling')
                    ri_zhu_yu_ri_zhi_wang_ruo = self.check_ri_zhu_yu_ling_you_li(from_ling='ri_zhi')
                    if ri_zhu_yu_ri_zhi_wang_ruo == ri_zhu_yu_nian_zhi_wang_ruo:
                        # 1.2.1.1.1 年支和日支对日主作用相同
                        self.ri_zhu_ling_wang_ruo = ri_zhu_yu_ri_zhi_wang_ruo
                    else:
                        # 1.2.1.1.2 年支和日支对日主的作用不同
                        self.ri_zhu_ling_wang_ruo = self.check_ri_zhu_yu_ling_you_li(from_ling='yue_ling')
            else:
                # 1.2.2 月令有力
                self.ri_zhu_ling_wang_ruo = self.check_ri_zhu_yu_ling_you_li(from_ling='yue_ling')
        # 1.2.2.3 得到的结果是不旺也不弱，则根据月干来
        if self.ri_zhu_ling_wang_ruo == TianGanShengYuLingWangRuo.不旺不弱:
            self.check_from_yue_gan = True
            self.ri_zhu_ling_wang_ruo = self.check_ri_zhu_yu_ling_you_li(from_ling='yue_gan')
        # 二、看天干是否从格
        self.cong_ge = self.check_cong_ge()
        # 三、根据实际情况
        self.ge_ju = self.get_ge_ju()

    def get_ge_ju(self) -> GeJu:
        """
        获取格局
        """
        if self.cong_ge and self.ri_zhu_ling_wang_ruo == TianGanShengYuLingWangRuo.弱:
            return GeJu.从弱
        elif self.cong_ge and self.ri_zhu_ling_wang_ruo == TianGanShengYuLingWangRuo.旺:
            return GeJu.从旺
        elif self.ri_zhu_ling_wang_ruo == TianGanShengYuLingWangRuo.弱:
            return GeJu.身弱
        elif self.ri_zhu_ling_wang_ruo == TianGanShengYuLingWangRuo.旺:
            return GeJu.身旺
        return GeJu.身弱

    def check_cong_ge(self) -> bool:
        """
        检查是否是从格
        """
        check_list = {"ri_zhi": "ri_zhu", "shi_gan": "shi_zhu", 'yue_gan': "yue_zhu"}
        for gan_zhi in check_list:
            zhu = check_list[gan_zhi]
            # 检查天干是否有根
            gan_you_li = self.check_tian_gan_you_gen(zhu)
            if gan_zhi == "ri_zhi":
                if gan_you_li:
                    # 日支干有力，就是日支起到了好作用，旺
                    ri_zhu_you_li = TianGanYuXiangLinGanZhiWangRuo.旺
                else:
                    # 日支干无力，就是日支起到了坏作用，弱
                    ri_zhu_you_li = TianGanYuXiangLinGanZhiWangRuo.弱
                # 因为日令无论如何都是有力的，因此常设置为True
                gan_you_li = True
            elif gan_zhi == 'yue_gan' and self.check_from_yue_gan:
                continue
            else:
                ri_zhu_you_li = self.check_ri_zhu_yu_xiang_lin_you_li(gan_zhi)
            if self.ri_zhu_ling_wang_ruo == TianGanShengYuLingWangRuo.弱:
                # 弱于月令、年令
                if ri_zhu_you_li == TianGanYuXiangLinGanZhiWangRuo.旺 and gan_you_li:
                    # 但是有力帮
                    return False
            else:
                # 旺于月令、年令
                if ri_zhu_you_li == TianGanYuXiangLinGanZhiWangRuo.弱 and gan_you_li:
                    # 但是有力制
                    return False
        return True

    def check_ri_zhu_yu_xiang_lin_you_li(self, position="ri_zhi") -> TianGanYuXiangLinGanZhiWangRuo:
        # TODO:判断相邻的干支对日主的旺弱
        return TianGanYuXiangLinGanZhiWangRuo.相邻干支无力

    def check_ling_shou_zhi_twice(self, ling="yue_ling") -> bool:
        """
        检查月令或者日令是否受制2次
        """
        if ling not in ['yue_ling', "ri_ling"]:
            raise "只检查月令和日令的受制情况"
        ling = self.pai_pan.yue_zhu.di_zhi
        if ling == 'ri_ling':
            ling = self.pai_pan.ri_zhu.di_zhi
        # TODO: 判断左右与令作用后是否受制两次
        return True

    def check_tian_gan_you_gen(self, target_position="") -> bool:
        """
        检查天干是否有根，有根就是有力
        """
        tian_gan = self.pai_pan.yue_zhu.tian_gan
        di_zhi = self.pai_pan.yue_zhu.di_zhi

        if target_position not in ['ri_zhu', "yue_zhu", "shi_zhu"]:
            pass
        if target_position == 'yue_zhu':
            # 月干有年支、年干、月支3个根
            pass
        # TODO:判断是否有根
        return True

    def check_ri_zhu_yu_ling_you_li(self, from_ling="yue_ling") -> TianGanShengYuLingWangRuo:
        """
        检查日柱在令是否有力
        """
        target = "ri_gan"
        if from_ling == "yue_ling":
            # 月令
            pass
        elif from_ling == "nian_ling":
            # 年令
            pass
        elif from_ling == "yue_gan":
            # 月干
            pass
        elif from_ling == "nian_gan":
            # 年干
            pass
        elif from_ling == 'ri_zhi':
            # 日支
            pass
        else:
            raise ("只能从月令、年令、月干、年干取")
        # TODO:判断令与日主的关系

    def check_yue_ling_kong_wang(self):
        """
        检查月令是否空亡
        """
        yue_ling = self.pai_pan.yue_zhu.di_zhi
        if yue_ling.name in [x.name for x in self.pai_pan.kong_wang]:
            return True
        else:
            return False
