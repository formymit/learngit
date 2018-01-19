#-*-coding:utf-8-*-
from config import basicConfig

myConfig = basicConfig()

with open(myConfig.inameCardNumFileName, encoding='UTF-8') as f:
    lines = f.readlines()
    print(len(lines))

    new_lines = set(lines)
    print(len(new_lines))


