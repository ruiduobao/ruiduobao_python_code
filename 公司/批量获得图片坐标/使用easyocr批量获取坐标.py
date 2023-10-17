from PIL import Image, ImageFilter
import pytesseract
import piexif
import os
from tqdm import tqdm
import easyocr
import re
import numpy as np

#纠正图片得到的经纬度信息
def correct_coordinates(longitude, latitude, lon_range=(108, 120), lat_range=(30, 38)):
    """
    Corrects the OCR-extracted longitude and latitude values based on the given ranges.
    """
    # Correct the longitude
    if longitude > lon_range[1] or longitude < lon_range[0]:
        longitude = longitude / 10**(len(str(int(longitude))) - len(str(int(lon_range[1]))))

    # Correct the latitude
    if latitude > lat_range[1] or latitude < lat_range[0]:
        latitude = latitude / 10**(len(str(int(latitude))) - len(str(int(lat_range[1]))))

    return longitude, latitude
#提取出来的数字标准化
def extract_and_sort_numbers(result):
    # 按照文本框的上边界排序结果
    result.sort(key=lambda item: min(point[1] for point in item[0]))

    # 提取文本并删除非数字字符
    numbers = [re.sub(r'\D', '', item[1]) for item in result]

    # 将字符串转换为整数
    numbers = [int(number) for number in numbers]

    return numbers
def write_lat_lon_to_exif(img_path, lat, lon):
    # Open the image file
    img = Image.open(img_path)

    # Check if the image has EXIF data
    if 'exif' in img.info:
        # Get the EXIF data
        exif_dict = piexif.load(img.info['exif'])
    else:
        # Create a new EXIF data dict
        exif_dict = {"0th":{},
                     "Exif":{},
                     "GPS":{},
                     "1st":{},
                     "thumbnail":None,
                     "Interop":{}
                    }

    # Convert the latitude and longitude to the format required by EXIF
    lat_deg = int(lat)
    lat_min = int((lat - lat_deg) * 60)
    lat_sec = (lat - lat_deg - lat_min / 60) * 3600

    lon_deg = int(lon)
    lon_min = int((lon - lon_deg) * 60)
    lon_sec = (lon - lon_deg - lon_min / 60) * 3600

    # Write the latitude and longitude to the EXIF data
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = [(lat_deg, 1), (lat_min, 1), (int(lat_sec * 10000), 10000)]
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = [(lon_deg, 1), (lon_min, 1), (int(lon_sec * 10000), 10000)]

    # Set the reference for latitude and longitude
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = 'N'
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = 'E'

    # Convert the EXIF data to bytes
    exif_bytes = piexif.dump(exif_dict)

    # Write the EXIF data to the image
    img.save(img_path, exif=exif_bytes)


# Write the coordinates to the image

def process_image(img_path):
    # text = pytesseract.image_to_string(img_dilated, lang='eng')
    reader = easyocr.Reader(['en'])  # this needs to run only once to load the model into memory
    # Open the image file
    img = Image.open(img_path)

    # Get the size of the image
    width, height = img.size

    # Define the coordinates of the box to crop as a ratio of the image size
    left_ratio = 322 / 2448
    top_ratio = 2200 / 3264
    right_ratio = 787 / 2448
    bottom_ratio = 2453 / 3264

    # Calculate the actual pixel coordinates
    left = int(left_ratio * width)
    top = int(top_ratio * height)
    right = int(right_ratio * width)
    bottom = int(bottom_ratio * height)

    # Crop the image
    img_cropped = img.crop((left, top, right, bottom))

    # Convert the image to grayscale
    img_gray = img_cropped.convert("L")

    # Convert the image to binary
    threshold = 128
    img_binary = img_gray.point(lambda x: 0 if x < threshold else 255, '1')

    # Apply a dilation operation to the image
    img_dilated = img_binary.filter(ImageFilter.MinFilter(3))

    # Convert the PIL image to a numpy array
    img_dilated_np = np.array(img_dilated).astype(np.uint8)

    # Pass the numpy array to easyocr
    result= reader.readtext(img_dilated_np * 255)  # Scale the pixel values back to the range [0, 255]
    print(result)
    # Pass the numpy array to easyocr
    # 检查是否得到了两个数字
    if len(result) != 2:
        return False

    longitude,latitude = result
    print('long:', longitude)
    print('lan:',  latitude)

    # Use pytesseract to do OCR on the image, replace 'chi_sim' with 'eng' if you're processing English text

    longitude,latitude = extract_and_sort_numbers(result)

    print('long:', longitude)
    print('lan:',  latitude)

    # Parse the text to float values
    # try:
    #     longitude, latitude = map(float, text.split())
    # except ValueError:
    #     return False

    # Correct the coordinates
    longitude, latitude = correct_coordinates(longitude, latitude)
    print(longitude, latitude)
    # Write the coordinates to the image
    write_lat_lon_to_exif(img_path, latitude, longitude)

    return True

# Process all images in the folder
folder_path = 'E:\公司\鹤壁_202307\鹤壁农作物采样点20230728\\2448_3264'
error_files = []
for filename in tqdm(os.listdir(folder_path)):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(folder_path, filename)
        print(img_path)
        if not process_image(img_path):
            error_files.append(img_path)

# Write the paths of the error files to a text file
with open('error_files.txt', 'w', encoding='utf-8') as f:
    for filepath in error_files:
        f.write("%s\n" % filepath)