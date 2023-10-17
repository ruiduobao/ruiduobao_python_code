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

PathA=r"F:\哥白尼DEM\全国各个县DEM"
image_path=r"F:\哥白尼DEM\\更多数据获取.jpg"

tif_paths=gma.osf.GetPath(PathA)
print(tif_paths)
for path in tqdm(tif_paths):
    folder_name=path.split("\\")[-1]
    #省级文件夹
    SHENG=folder_name.split("_")[0]
    #地级文件夹
    SHI=folder_name.split("_")[1]
    #县级文件夹
    XIAN=folder_name.split("_")[2].replace(".tif","")
    #文件名
    file_NAME=os.path.basename(path).replace(".tif","_哥白尼DEM_公众号遥感之家.tif")
    print(file_NAME)
    #完整文件夹路径
    FOLDER_PATH=PathA+"\\"+SHENG+"\\"+SHI+"\\"+XIAN+"\\"
    print(FOLDER_PATH)
    create_folder_if_not_exists(FOLDER_PATH)
    # 完整文件夹路径
    FILE_PATH = FOLDER_PATH + file_NAME
    print(FILE_PATH)
    #移动文件夹
    shutil.move(path, FOLDER_PATH)
    #将二维码移动到每个文件夹中
    shutil.copy(image_path, FOLDER_PATH)

