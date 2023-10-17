import re


def extract_and_sort_numbers(result):
    # 按照文本框的上边界排序结果
    result.sort(key=lambda item: min(point[1] for point in item[0]))

    # 提取文本并删除非数字字符
    numbers = [re.sub(r'\D', '', item[1]) for item in result]

    # 将字符串转换为整数
    numbers = [int(number) for number in numbers]

    return numbers


result = [([[31, 25], [359, 25], [359, 89], [31, 89]], '114140133', 0.7645970026566759),
          ([[29, 113], [353, 113], [353, 177], [29, 177]], '36,018047', 0.7806329155698005)]

long, lan = extract_and_sort_numbers(result)

print('long:', long)
print('lan:', lan)