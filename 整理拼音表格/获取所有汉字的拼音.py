import os
import pypinyin
import itertools

# 获取所有的汉字
all_chinese_characters = [chr(i) for i in range(0x4e00, 0x9fff)]

# 将汉字转换为拼音
pinyin_list = []
for character in all_chinese_characters:
    pinyin = pypinyin.lazy_pinyin(character)
    pinyin_list.extend(pinyin)

# 去除重复的拼音
unique_pinyin = sorted(set(pinyin_list))

# 将拼音列表转换为逗号分隔的字符串
pinyin_string = ",".join(unique_pinyin)

# 保存到文件
with open("pinyin.txt", "w", encoding="utf-8") as file:
    file.write(pinyin_string)

print("Pinyin saved to pinyin.txt")
