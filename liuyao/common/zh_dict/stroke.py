import os


def get_stroke(c):
    # 如果返回 0, 则也是在unicode中不存在kTotalStrokes字段
    strokes = []
    txt_file_path = os.path.abspath(__file__).replace(".py", ".txt")
    with open(txt_file_path, 'r') as fr:
        for line in fr:
            strokes.append(int(line.strip()))

    unicode_ = ord(c)

    if 13312 <= unicode_ <= 64045:
        return strokes[unicode_ - 13312]
    elif 131072 <= unicode_ <= 194998:
        return strokes[unicode_ - 80338]
    else:
        return None
