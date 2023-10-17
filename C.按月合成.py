import gma
import os
import shutil
from tqdm import tqdm
import get_path_from_DIR

IMAGES_START_PATH="D:\\云量数据\\B按时间归类_21年缺失\\"
IMAGES_OUTPUT_PATH="D:\\云量数据\\C按月合成\\"
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
    #获取以及循环月文件夹
    MONTH_FOLDERS = get_path_from_DIR.get_DirS_path(YEAR_FOLDER)
    for MONTH_FOLDER in tqdm(MONTH_FOLDERS):
        try:
            MONTH = MONTH_FOLDER.split("\\")[-1]
            # 创建月文件夹
            MONTH_OUTPUT_FOLDER = YEAR_OUTPUT_FOLDER + MONTH + "\\"
            mkdir(MONTH_OUTPUT_FOLDER)
            #获取影像，并镶嵌
            TIFS = get_path_from_DIR.get_suffix_path(MONTH_FOLDER+"\\",".tif")
            OUTPUT_NAME =YEAR_OUTPUT_FOLDER+YEAR+"_"+MONTH+".tif"
            gma.rasp.Mosaic(TIFS, OUTPUT_NAME)
            gma.rasp.GenerateOVR(OUTPUT_NAME)
        except:
            print(MONTH_FOLDER)