import pandas as pd
import requests

url = "https://dmfw.mca.gov.cn/foreign/getForeignList?searchValue=cheng&pageNum=1&pageSize=10000"
response = requests.get(url)
data = response.json()

# 直接将'data'键对应的列表作为DataFrame的数据
df = pd.DataFrame(data['data'])

# 将DataFrame保存为Excel文件
df.to_excel('output222.xlsx', index=False)
