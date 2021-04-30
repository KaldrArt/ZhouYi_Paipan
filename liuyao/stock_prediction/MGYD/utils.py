from liuyao.common.zh_dict.stroke import get_stroke

alphabets = " abcdefghijklmnopqrstuvwxyz"
nums = "0123456789"


def stock_id_code(stock_id):
    pass


def name_code(name):
    unicode_count = []
    stroke_count_and_alphabet_index = []
    for char in name:
        unicode = ord(char)
        unicode_count.append(unicode)
        char = char.lower()
        if char in alphabets:
            stroke_count_and_alphabet_index.append(alphabets.index(char))
        elif char in nums:
            stroke_count_and_alphabet_index.append(nums.index(char))
        else:
            n = get_stroke(char)  # 括号等没有笔画
            if n:
                stroke_count_and_alphabet_index.append(n)
    return {
        "unicode_count": unicode_count,
        "stroke_count_and_alphabet_index": stroke_count_and_alphabet_index
    }


def get_stock_name_shu(name, stock_id):
    code = name_code(name)
    code['stock_code'] = stock_id_code(stock_id)
    return code
