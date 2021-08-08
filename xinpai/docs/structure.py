basic_step_names = [
    "相邻天干之间",
    "地支对天干",
    '相邻地支',
    '天干生于月令',
    "天干生于年令",
    "天干生于月干",
    "天干生于年干"
]


class Structure:
    """
    解释新派八字断法的程序
    """
    stages = {
        "basic": {
            "index": 1,
            "name": "基础",
            "steps": {
                "ming_ju_gan_zhi": {
                    "index": 1,
                    "name": "命局干支作用规律",
                    "rules": {
                        
                    }
                },
                "da_yun_liu_nian_gan_zhi": {
                    "index": 2,
                    "name": "大运流年干支作用规律",
                    "rules": {

                    }
                }
            }
        },
        "geju": {
            "index": 2,
            "name": "格局判定",
            "steps": {
                "ri_gan_wang_ruo": {
                    "index": 1,
                    "name": "日干生于令的旺弱"
                },
                "cong": {
                    "index": 2,
                    "name": "日主是否从格"
                }
            }
        },
        "mingju": {
            "index": 3,
            "name": "命局分析"
        },
        "dayun": {
            "index": 4,
            "name": "大运流年分析"
        }
    }

    def __init__(self):
        pass
