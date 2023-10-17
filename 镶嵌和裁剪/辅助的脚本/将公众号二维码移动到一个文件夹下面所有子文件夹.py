import os
import gma
from tqdm import tqdm
import shutil

# os.rename("D:\\demo\\a.txt","D:\\demo\\b.txt")
# print("重命名完毕")
def create_folder_if_not_exists(folder_path):
    """
    创建文件夹（如果不存在）。

    :param folder_path: 要创建的文件夹的路径
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"文件夹 '{folder_path}' 已创建。")
    else:
        print(f"文件夹 '{folder_path}' 已经存在，不需要创建。")

PathA=r"F:\哥白尼DEM\分省\\"
tif_paths=gma.osf.GetPath(PathA,Search  = 'DIR')
tif_paths=tif_paths[1:]

image_path=r"F:\哥白尼DEM\\更多数据获取.jpg"

for path in tqdm(tif_paths):
    shutil.copy(image_path, path)
