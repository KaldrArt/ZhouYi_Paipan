from datetime import datetime

default_info = {
    "datetime": datetime.now(),
    "tz": "+08",
    "age": 0,
    "profession": "",
    "category": "",
    "condition": "",
    "time_limit": 0,
    "time_limit_type": "天",
    "prediction_content": ""
}

default_yang_count = [0, 0, 0, 0, 0, 0]


class PaiPan:
    def __init__(self, code=default_yang_count, info=default_info):
        self.code = code
        self.info = info
        if self.check_paipan_info():
            self.get_pai_pan()
        
    def check_paipan_info(self):
        pass

    def get_ri_yue_shi_fen(self):
        pass

    def get_basic_info(self):
        pass

    def get_pai_pan(self):
        pass
