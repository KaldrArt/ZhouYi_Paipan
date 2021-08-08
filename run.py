from analyzer.basic_analyzer import BasicAnalyzer

# BasicAnalyzer('1980/1/14 3:35', gender=False)  # 克夫女
# BasicAnalyzer('1972/7/3 13:15', False)  # 克夫尼姑女
# BasicAnalyzer("1987/10/13 9:35", True)
# BasicAnalyzer("1987/8/12 17:18", True)
# BasicAnalyzer("1988/12/29 22:18", False)
# BasicAnalyzer("2021/3/20 11:35", False)
# BasicAnalyzer('1979/10/23 17:30', False)
# BasicAnalyzer('1953/5/7 11:00', False)
# BasicAnalyzer("2003/7/23 21:00", True)  # 戊午运丁酉年和同学打游戏打架被学校辍学，身弱杀旺
# BasicAnalyzer("1979/5/2 9:00", True)  # 甲子运庚子年，肝癌，3月检查出来，10月去世
# BasicAnalyzer('1970/8/11 13:00', True)  # 身旺格局，原局伤官见官了，如果官杀混杂，给日主加力，就更加容易出事情。戊子运戊戌年，得了白血病，庚子年去世
# BasicAnalyzer("1993/10/14 15:00", False)  # 身旺克官，甲子运庚子年伤官见官，男朋友车祸
# BasicAnalyzer("1988/1/7 17:00", False)
# BasicAnalyzer("1955/10/30 21:00", True)
# BasicAnalyzer("1952/1/1 17:00",False)
# BasicAnalyzer("1996/4/1 04:55", False) # 邵心怡
# BasicAnalyzer('1973/5/9 19:00:00', True) # 癸丑运，癸巳年父亲去世，壬辰年儿子去世。癸丑使得癸水有根，所以所以身弱，而不是从弱。
# 比劫太旺，惹怒了官杀，水土大战。戊申运，己亥年，申子辰三合水，亥子丑三会水，官杀混杂，车祸死了。
a = BasicAnalyzer('1973/1/6 8:00:00', False)
