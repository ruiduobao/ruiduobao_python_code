import gma
import os
import shutil
from tqdm import tqdm
import get_path_from_DIR

IMAGES_START_PATH="E:\keshan\云量实验\C按月合成\\"
IMAGES_OUTPUT_PATH="E:\keshan\云量实验\E求逐年平均\\"
#创建各地文件夹函数
def mkdir(path):
    # 引入模块
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        # print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(path + ' 目录已存在')
        return False
#获取年文件夹
YEAR_FOLDERS=get_path_from_DIR.get_DirS_path(IMAGES_START_PATH)
for YEAR_FOLDER in YEAR_FOLDERS:
    YEAR =YEAR_FOLDER.split("\\")[-1]
    #创建年文件夹
    YEAR_OUTPUT_FOLDER=IMAGES_OUTPUT_PATH+YEAR+"\\"
    mkdir(YEAR_OUTPUT_FOLDER)
    #获取影像，并相加
    TIFS = get_path_from_DIR.get_doublesuffix_path(YEAR_FOLDER,".tif")
    OUTPUT_NAME =YEAR_OUTPUT_FOLDER+YEAR+".tif"
    #对获取到的影像求平均值
    gma.rasp.Mosaic(TIFS, OUTPUT_NAME)
    gma.rasp.GenerateOVR(OUTPUT_NAME)