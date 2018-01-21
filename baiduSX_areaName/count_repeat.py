#-*-coding:utf-8-*-
from config import basicConfig

myConfig = basicConfig()

with open('keyWords', 'r') as f:
    lines = f.readlines()
    print(len(lines))

    new_lines = set(lines)
    print(len(new_lines))
    for each in new_lines:
        print len(each)
        with open('kw_words', 'a') as f2:
            if len(each) == 7:
                print each
                f2.write(each)


