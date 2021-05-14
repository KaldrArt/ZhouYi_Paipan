from liuyao.common.zh_dict.stroke import get_stroke

alphabets = " abcdefghijklmnopqrstuvwxyz"
nums = "0123456789"

def name_code(name):
    unicode_count = []
    stroke_count_and_alphabet_index = []
    for char in name:
        unicode = ord(char)
        unicode_count.append(unicode)
        char = char.lower()
        if char in alphabets:
            # 字母取字母的位置，例如a是1，b是2
            stroke_count_and_alphabet_index.append(alphabets.index(char))
        elif char in nums:
            # 数字取数字的位置代表的数，例如0是0,1是1
            stroke_count_and_alphabet_index.append(nums.index(char))
        else:
            n = get_stroke(char)  # 括号等没有笔画
            if n:
                stroke_count_and_alphabet_index.append(n)
    return {
        "unicode_count": unicode_count,
        "basic_count": stroke_count_and_alphabet_index
    }



def stock_id_code(stock_id):
    return name_code(stock_id)


def get_stock_shu(name, stock_id, with_short_prefix=False):
    return {
        'stock_name': name_code(name),
        'stock_id': stock_id_code(stock_id if with_short_prefix else stock_id[2:])
    }
