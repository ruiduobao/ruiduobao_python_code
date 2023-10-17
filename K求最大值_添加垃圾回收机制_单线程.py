import os
import numpy as np
from osgeo import gdal
from tqdm import tqdm
import gc
from multiprocessing import Pool
import uuid
import shutil


root_folder = r"F:\\INPUT3\\"
output_folder = r"F:\\MIDDATA\\"
# 设置移动目标文件夹路径
destination_folder = r"E:\\cloud\\output\\"
# root_folder = r"D:\\keshan\\gdal\\代求\\"
# output_folder = r"D:\\keshan\\gdal\\结果\\"



subfolders = [subfolder for subfolder in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, subfolder))]
for subfolder in subfolders:
    try:
        subfolder_path = os.path.join(root_folder, subfolder)
        if os.path.isdir(subfolder_path):
            files = [f for f in os.listdir(subfolder_path) if f.endswith('.tif')]

            first = os.path.join(subfolder_path, files[0])
            src_ds = gdal.Open(first.encode('utf-8'))
            x_size = src_ds.RasterXSize
            y_size = src_ds.RasterYSize
            data_type = src_ds.GetRasterBand(1).DataType
            projection = src_ds.GetProjection()
            geotransform = src_ds.GetGeoTransform()

            output_file = os.path.join(output_folder, f"{subfolder}.tif")
            driver = gdal.GetDriverByName("GTiff")
            dst_ds = driver.Create(output_file, x_size, y_size, 1, gdal.GDT_Int16, options=["COMPRESS=DEFLATE", "BIGTIFF=YES"])
            dst_ds.SetProjection(projection)
            dst_ds.SetGeoTransform(geotransform)

            # 修改分块大小，将图像分为更多的网格，以减小每个进程的内存需求
            x_block_size = x_size // 4
            y_block_size = y_size // 4

            for x_offset in tqdm(range(0, x_size, x_block_size), desc=f"Processing {subfolder} x_block_size"):
                for y_offset in range(0, y_size, y_block_size):
                    block_width = min(x_block_size, x_size - x_offset)
                    block_height = min(y_block_size, y_size - y_offset)

                    dtype = np.int32
                    mmap_filename = f'mmap_{uuid.uuid4().hex}.bin'
                    mmap_array = np.memmap(mmap_filename, dtype=dtype, mode='w+', shape=(block_height, block_width))

                    first_iteration = True
                    for file_name in files:
                        file_path = os.path.join(subfolder_path, file_name)
                        src_ds = gdal.Open(file_path)
                        array = src_ds.GetRasterBand(1).ReadAsArray(x_offset, y_offset, block_width, block_height)
                        array = array.astype('int32')

                        if first_iteration:
                            mmap_array[:] = array[:]
                            first_iteration = False
                        else:
                            mmap_array[:] = np.maximum(mmap_array, array)

                        src_ds = None

                    max_array = mmap_array.astype(np.int16)
                    out_band = dst_ds.GetRasterBand(1)
                    out_band.WriteArray(max_array, xoff=x_offset, yoff=y_offset)

                    del mmap_array  # 删除 mmap_array 变量，以确保文件不再被使用
                    os.unlink(mmap_filename)  # 在这里删除内存映射文件
                    del max_array, out_band, array
                    gc.collect()
            dst_ds = None
            #移动文件到机械硬盘
            destination_file = os.path.join(destination_folder, f"{subfolder}.tif")
            shutil.move(output_file, destination_file)

            #保存信息
            error_message = f"{output_file} GO_sucess: "

            print(error_message)

            # 将成功信息保存到log.txt

            error_log_path = r"E:\cloud\output\log.txt"

            with open(error_log_path, "a") as error_log:
                error_log.write(error_message + "\n")


    except Exception as e:

            error_message = f"{subfolder} GO_WRONG: {str(e)}"
            print(error_message)
            # 将错误信息保存到log.txt
            error_log_path = os.path.join(destination_folder, "log.txt")
            with open(error_log_path, "a") as error_log:
                error_log.write(error_message + "\n")