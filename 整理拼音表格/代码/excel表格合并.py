import pandas as pd
import os

# 获取所有Excel文件的列表
folder_path = 'E:\\code\\整理拼音表格\\获得的excel表格分散'  # 替换为你的文件夹路径
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# 读取并合并所有Excel文件
all_data = pd.DataFrame()
for file in excel_files:
    df = pd.read_excel(os.path.join(folder_path, file))
    all_data = pd.concat([all_data, df])

# 将合并的DataFrame保存为一个新的Excel文件
all_data.to_excel('merged.xlsx', index=False)
