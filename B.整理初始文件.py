import gma
import os
import shutil
from tqdm import tqdm

IMAGES_START_PATH="G:\\我的云端硬盘\\ESAT_ASIA_CLOUD\\"
IMAGES_OUTPUT_PATH="D:\\云量数据\\B按时间归类\\"
images_ready_todo=gma.osf.GetPath(IMAGES_START_PATH, EXT = '.tif')


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
#年
YEAR = []
#月
MONTH = []

for image_ready_todo in tqdm(images_ready_todo):
    # print(image_ready_todo)
    image_name=image_ready_todo.split("ESAT_ASIA_CLOUD\\")[-1]
    # print(image_name)
    year=image_name.split("_")[1]
    # print(year)
    if year not in YEAR:
        YEAR.append(year)
    month = image_name.split("_")[2].split("-")[0]
    if month not in MONTH:
        MONTH.append(month)
    #创建年文件夹
    DIR_NAME=IMAGES_OUTPUT_PATH+year
    mkdir(DIR_NAME)
    # 创建月文件夹
    DIR_NAME=IMAGES_OUTPUT_PATH+year+"\\"+month
    mkdir(DIR_NAME)
    #移动数据到指定年份的文件夹
    dst_filename = DIR_NAME+"\\"+image_name
    # print(dst_filename)
    # 使用shutil.copyfile()方法复制文件到目标文件夹中，并指定目标文件名
    shutil.copyfile(image_ready_todo, dst_filename)