from liuyao.common.paipan.paipan import PaiPan

info = {
    "年龄": "中年",
    "性别": "男",
    "职业": "无",
    "预测策项": "股票走势",
    "起卦钥语": "股票走势",
    "前提条件": "暂无",
    "策项时限": "一天",
    "起卦时间": "SY案例"
}
# 第一课
example001 = PaiPan(444, "壬辰", "丙辰", info)
# example001.print_md()
example002 = PaiPan(544, "壬辰", "丁巳", info)
# example002.print_md()
example003 = PaiPan(584, "辛卯", "乙酉", info)
example003.print_md()
