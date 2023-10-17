import os
import shutil
from PIL import Image

# The path to the folder that contains the images
folder_path = 'E:\公司\鹤壁_202307\鹤壁农作物采样点20230728\鹤壁农作物采样点20230728'

# The paths to the subfolders for the two types of images
subfolder_path_1 = 'E:\公司\鹤壁_202307\鹤壁农作物采样点20230728\\2448_3264'
subfolder_path_2 = 'E:\公司\鹤壁_202307\鹤壁农作物采样点20230728\\3264_2448'
subfolder_path_other="E:\公司\鹤壁_202307\鹤壁农作物采样点20230728\其他分辨率"
# Create the subfolders if they don't exist
os.makedirs(subfolder_path_1, exist_ok=True)
os.makedirs(subfolder_path_2, exist_ok=True)

# Go through all the images in the folder
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Open the image and get its size
        img_path = os.path.join(folder_path, filename)
        img = Image.open(img_path)
        width, height = img.size

        # Move the image to the appropriate subfolder
        if width == 2448 and height == 3264:
            shutil.copy(img_path, os.path.join(subfolder_path_1, filename))
        elif width == 3264 and height == 2448:
            shutil.copy(img_path, os.path.join(subfolder_path_2, filename))
        else:
            shutil.copy(img_path, os.path.join(subfolder_path_other, filename))