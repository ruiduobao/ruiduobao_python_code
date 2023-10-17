from PIL import Image, ImageFilter
import piexif
import os
from tqdm import tqdm
import easyocr
import re
import numpy as np
import shutil

# 定义函数...
# 纠正OCR提取的经纬度信息
def correct_coordinates(longitude, latitude, lon_range=(108, 120), lat_range=(30, 38)):
    """
    纠正OCR提取的经纬度值，根据给定的范围
    """
    # 纠正经度
    if longitude > lon_range[1] or longitude < lon_range[0]:
        longitude = longitude / 10**(len(str(int(longitude))) - len(str(int(lon_range[1]))))

    # 纠正纬度
    if latitude > lat_range[1] or latitude < lat_range[0]:
        latitude = latitude / 10**(len(str(int(latitude))) - len(str(int(lat_range[1]))))

    return longitude, latitude

# 提取并排序数字
def extract_and_sort_numbers(result):
    """
    从OCR结果中提取数字，并进行排序
    """
    # 按照文本框的上边界排序结果
    result.sort(key=lambda item: min(point[1] for point in item[0]))

    # 提取文本并删除非数字字符
    numbers = [re.sub(r'\D', '', item[1]) for item in result]

    # 将字符串转换为整数
    numbers = [int(number) for number in numbers]

    return numbers

# 将经纬度信息写入图片的EXIF
def write_lat_lon_to_exif(img_path, lat, lon):
    """
    将经纬度信息写入图片的EXIF
    """
    # 打开图片文件
    img = Image.open(img_path)

    # 检查图片是否有EXIF数据
    if 'exif' in img.info:
        # 获取EXIF数据
        exif_dict = piexif.load(img.info['exif'])
    else:
        # 创建一个新的EXIF数据字典
        exif_dict = {"0th":{},
                     "Exif":{},
                     "GPS":{},
                     "1st":{},
                     "thumbnail":None,
                     "Interop":{}
                    }

    # 将经纬度转换为EXIF需要的格式
    lat_deg = int(lat)
    lat_min = int((lat - lat_deg) * 60)
    lat_sec = (lat - lat_deg - lat_min / 60) * 3600

    lon_deg = int(lon)
    lon_min = int((lon - lon_deg) * 60)
    lon_sec = (lon - lon_deg - lon_min / 60) * 3600

    # 将经纬度写入EXIF数据
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = [(lat_deg, 1), (lat_min, 1), (int(lat_sec * 10000), 10000)]
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = [(lon_deg, 1), (lon_min, 1), (int(lon_sec * 10000), 10000)]

    # 设置经纬度的参考
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = 'N'
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = 'E'

    # 将EXIF数据转换为字节
    exif_bytes = piexif.dump(exif_dict)

    # 将EXIF数据写入图片
    img.save(img_path, exif=exif_bytes)

# 处理图片
def process_image(img_path):
    """
    处理图片，包括OCR提取经纬度，纠正经纬度，并将经纬度写入图片的EXIF
    """
    # 创建一个OCR reader
    reader = easyocr.Reader(['en'])  # 这只需要运行一次，用于将模型加载到内存中

    # 打开图片文件
    img = Image.open(img_path)

    # 获取图片的尺寸
    width, height = img.size

    # 定义裁剪框的坐标，作为图片尺寸的比例
    left_ratio = 322 / 2448
    top_ratio = 2200 / 3264
    right_ratio = 787 / 2448
    bottom_ratio = 2453 / 3264

    # 计算实际的像素坐标
    left = int(left_ratio * width)
    top = int(top_ratio * height)
    right = int(right_ratio * width)
    bottom = int(bottom_ratio * height)

    # 裁剪图片
    img_cropped = img.crop((left, top, right, bottom))

    # 将图片转换为灰度图
    img_gray = img_cropped.convert("L")

    # 将图片转换为二值图
    threshold = 90
    img_binary = img_gray.point(lambda x: 0 if x < threshold else 255, '1')

    # 对图片进行扩张操作
    img_dilated = img_binary.filter(ImageFilter.MinFilter(3))

    # 将PIL图像转换为numpy数组
    img_dilated_np = np.array(img_dilated).astype(np.uint8)

    # 将numpy数组传递给easyocr
    result = reader.readtext(img_dilated_np * 255)  # 将像素值扩展回范围[0, 255]
    print(result)

    # 检查是否得到了两个数字
    if len(result) != 2:
        return False

    longitude, latitude = result
    print('long:', longitude)
    print('lan:', latitude)

    longitude, latitude = extract_and_sort_numbers(result)
    print('long:', longitude)
    print('lan:', latitude)

    # 纠正坐标
    longitude, latitude = correct_coordinates(longitude, latitude)
    print(longitude, latitude)

    # Check if the corrected coordinates are within the valid range
    if (not 108 <= longitude <= 120) or (not 30 <= latitude <= 38):
        return False

    # 将坐标写入图片
    write_lat_lon_to_exif(img_path, latitude, longitude)

    return True
def main():
    # 处理文件夹中的所有图片
    # Process all images in the folder
    folder_path = 'E:\公司\鹤壁_202307\鹤壁农作物采样点20230728\\2448_3264'
    error_files = []
    success_path = 'E:\公司\鹤壁_202307\鹤壁农作物采样点20230728\\2448_3264成功读取'
    failure_path = 'E:\公司\鹤壁_202307\鹤壁农作物采样点20230728\\2448_3264未成功读取'

    for filename in tqdm(os.listdir(folder_path)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            print(img_path)
            if not process_image(img_path):
                error_files.append(img_path)
                shutil.copy2(img_path, failure_path)  # 复制未成功识别的图片到指定路径
            else:
                shutil.copy2(img_path, success_path)  # 复制成功识别的图片到指定路径



    # 将错误文件的路径写入文本文件
    with open('error_files.txt', 'w', encoding='utf-8') as f:
        for filepath in error_files:
            f.write("%s\n" % filepath)

if __name__ == "__main__":
    main()