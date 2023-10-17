
# 打开并读取txt文件
with open("pinyin.txt", "r", encoding="utf-8") as file:
    content = file.read()

# 使用逗号作为分隔符将内容拆分成拼音列表
pinyin_list = content.split(",")

# 逐个处理拼音
for pinyin in pinyin_list:
    URL_1 = "https://dmfw.mca.gov.cn/foreign/getForeignList?searchValue="
    URL_2 = "&pageNum=1&pageSize=1000000"
    URL = URL_1 +pinyin+URL_2
    print(URL)


