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


def get_sim_word_with_strokes(stroke_count, max=100):
    strokes = []
    txt_file_path = os.path.abspath(__file__).replace(".py", ".txt")
    with open(txt_file_path, 'r') as fr:
        line_idx = 0
        for line in fr:
            if len(strokes) >= max:
                break
            elif 40869 >= line_idx >= 19968:
                if int(line.strip()) == stroke_count:
                    strokes.append(line_idx)
            line_idx += 1
    for s in strokes:
        print(chr(s + 13312))

# get_sim_word_with_strokes(12)
