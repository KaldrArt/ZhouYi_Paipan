from analyzer.basic_analyzer import BasicAnalyzer
import sys

if __name__ == '__main__':
    if len(sys.argv) == 3:
        print()
        date = sys.argv[1].replace("T", " ")
        gender = True if sys.argv[2] == '1' else False
        BasicAnalyzer(date, gender)

    else:
        pass
