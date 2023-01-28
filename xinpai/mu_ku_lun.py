from bazi_common import *
from enum import Enum


class MuKuPosition(Enum):
    月令 = "月令"
    年令 = "年令"
    大运 = "大运"
    流年 = "流年"
    地支 = "地支"
    月干根 = "月干根"


class MuKuLun:
    """
    新派墓库论是十分重要的内容。
    土是五行中最为特殊的一种五行。十二长生指的是天干在地支的长生。而土是所有其他四行的墓库。
    新派里，土不一定生金，而且不一定克水。
    """
    mu_ku = "辰戌丑未"
    # 地支为辰戌丑未土时，天干的旺衰情况
    tong_zhu_wang_shuai = {
        "辰": [-1, -1, -1, -1, 1, 1, 1, 1, 1, 1],  # √
        "戌": [-1, -1, 1, 1, 1, 1, -1, -1, -1, -1],  # √
        "丑": [-1, -1, -1, -1, 1, 1, 1, 1, 1, 1],  # √
        "未": [-1, -1, 1, 1, 1, 1, -1, -1, -1, -1]  # √
    }
    # 日主生于辰戌丑未月时的旺衰
    yue_ling_wang_shuai = {
        "辰": [-1, -1, -1, -1, 0, 0, 1, 1, 0, 0],  # √
        "戌": [-1, -1, 0, 0, 0, 1, -1, -1, -1, -1],  # √
        "丑": [-1, -1, -1, -1, 0, 0, 0, 1, 0, 1],  # √
        "未": [-1, -1, 0, 1, 1, 1, -1, -1, -1, -1]  # √
    }
    # 月令空亡，日主生于辰戌丑未年
    nian_zhi_wang_shuai = {
        "辰": [-1, -1, -1, -1, 0, 0, 1, 1, 0, 0],
        "戌": [-1, -1, 0, 0, 0, 1, -1, -1, -1, -1],
        "丑": [-1, -1, -1, -1, 1, 0, 0, 1, 0, 1],
        "未": [-1, -1, 0, 1, 1, 1, -1, -1, -1, -1]
    }

    def check_dizhi_is_muku(self, di_zhi: DiZhiBase):
        if di_zhi.name in self.mu_ku:
            return True
        else:
            raise BaseException("输入的地支[ %s ]不是墓库" % di_zhi.name)

    def get_mu_ku_tian_gan_wang_shuai_list(self, mu_ku_position: MuKuPosition):
        if mu_ku_position == MuKuPosition.地支:
            return self.tong_zhu_wang_shuai
        elif mu_ku_position == MuKuPosition.年令:
            return self.nian_zhi_wang_shuai
        elif mu_ku_position == MuKuPosition.月令:
            return self.yue_ling_wang_shuai
        elif mu_ku_position == MuKuPosition.月干根:
            pass
        else:
            return self.yi_ban_wang_shuai

    def get_mu_ku_di_zhi_wang_shuai_list(self):
        pass

    def check_tian_gan_wamg_shuai(self,
                                  tian_gan: TianGanBase,
                                  mu_ku: DiZhiBase,
                                  mu_ku_position: MuKuPosition):
        if self.check_dizhi_is_muku(mu_ku):
            tian_gan_index = tian_gan.index
            mu_ku_name = mu_ku.name

    def check_di_zhi_wang_shuai(self,
                                di_zhi: TianGanBase,
                                mu_ku: DiZhiBase,
                                mu_ku_position: MuKuPosition):
        if self.check_dizhi_is_muku(mu_ku):
            pass

    def get_uncertain_info(self):
        pass
