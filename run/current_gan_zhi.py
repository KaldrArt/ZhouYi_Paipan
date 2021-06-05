from datetime import datetime
from paipan.si_zhu import SiZhu

if __name__ == '__main__':
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")
    print(SiZhu(now).bazi.replace("乾造: ", "").replace("坤造: ", ""))
