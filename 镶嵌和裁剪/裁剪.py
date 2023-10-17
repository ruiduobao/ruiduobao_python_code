import gma
from tqdm import tqdm

InFile=r"F:\哥白尼DEM\全国DEM数据\全国哥白尼DEM数据.tif"
PathA=r"E:\code\镶嵌和裁剪\2023年县级\split\\"
OutFile=r"F:\哥白尼DEM\全国各个县DEM\\"
tif_paths=gma.osf.GetPath(PathA, EXT = '.gpkg')
for path in tqdm(tif_paths):
    name=path.split("\\")[-1].replace('.gpkg','')
    print(name)
    NAME = OutFile+name+".tif"
    gma.rasp.Clip(InFile, NAME, path)
