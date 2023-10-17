import pandas as pd
import requests
from tqdm import tqdm

#输出路径
OUTPUT_PATH=r"E:\code\整理拼音表格\输出文件\\"

# 打开并读取txt文件
with open("pinyin - 副本.txt", "r", encoding="utf-8") as file:
    content = file.read()

# 使用逗号作为分隔符将内容拆分成拼音列表
pinyin_list = content.split(",")

# 逐个处理拼音
for pinyin in tqdm(pinyin_list):
    try:
        URL_1 = "https://dmfw.mca.gov.cn/foreign/getForeignList?searchValue="
        URL_2 = "&pageNum=1&pageSize=1000000000"
        URL = URL_1 +pinyin+URL_2
        response = requests.get(URL)
        data = response.json()
        # 直接将'data'键对应的列表作为DataFrame的数据
        df = pd.DataFrame(data['data'])
        # 将DataFrame保存为Excel文件
        OUTPUT_EXCEL=OUTPUT_PATH+pinyin+".xlsx"
        df.to_excel(OUTPUT_EXCEL, index=False)
    except:
        print(pinyin)
