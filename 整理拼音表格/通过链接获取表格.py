import requests
import pandas as pd

# 请求数据
url = "https://dmfw.mca.gov.cn/foreign/getForeignList?searchValue=cheng&pageNum=1&pageSize=10000"
response = requests.get(url)
data = response.json()

# 将数据转化为pandas DataFrame
df = pd.DataFrame(data["data"])

# 将DataFrame保存为Excel文件
df.to_excel("output2.xlsx", index=False)
