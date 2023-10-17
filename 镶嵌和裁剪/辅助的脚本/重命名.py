import os
import gma
from tqdm import tqdm


# os.rename("D:\\demo\\a.txt","D:\\demo\\b.txt")
# print("重命名完毕")

PathA=r"E:\code\镶嵌和裁剪\2023年县级\split\\"

tif_paths=gma.osf.GetPath(PathA, EXT = '.gpkg')
print(tif_paths)
for path in tqdm(tif_paths):
    # tif_name=path.split("\\")[-1]
    # print(tif_name)
    # OutFile=OUTPUT_PATH+tif_name
    #
    # NAME=tif_name.replace("——哥白尼DEM——省_","")
    path2 = path.replace("FULL_NAME_", "")
    # NAME=PathA+NAME
    os.rename(path, path2)
    # print(NAME)
