#获取一个总文件夹下面的子文件夹中的某个格式的文件路径列表
import os
import pathlib

#一级目录筛选
def get_suffix_path(DIR_Path,suffix):
    TIF_path=[]
    #文件
    files_path = os.listdir(DIR_Path)
    for file in files_path:
        # 市目录
        file_PATH = os.path.join(DIR_Path, file)
        file_suffix=pathlib.Path(file_PATH).suffix
        if file_suffix==suffix:
            TIF_path.append(file_PATH)
    return TIF_path

#二级目录筛选
def get_doublesuffix_path(DIR_Path,suffix):
    TIF_path=[]
    #目录列表
    folder_Paths = os.listdir(DIR_Path)
    #重命名文件
    # 循环
    for folder_Path in folder_Paths:
        #目录
        dirs_path= os.path.join(DIR_Path, folder_Path)
        #文件
        files_path = os.listdir(dirs_path)
        for file in files_path:
            # 市目录
            file_PATH = os.path.join(dirs_path, file)
            file_suffix=pathlib.Path(file_PATH).suffix
            if file_suffix==suffix:
                TIF_path.append(file_PATH)
    return TIF_path
#获取文件夹下的文件夹
def get_DirS_path(DIR_Path):
    DIR_paths_list = []
    Dirs_paths = os.listdir(DIR_Path)
    for Dir_path in Dirs_paths:
        dirs_path = os.path.join(DIR_Path, Dir_path)
        DIR_paths_list.append(dirs_path)
    return DIR_paths_list
