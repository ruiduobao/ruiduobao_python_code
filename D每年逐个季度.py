import os
import numpy as np
from osgeo import gdal
from tqdm import tqdm

# root_folder = r"C:\\云量数据\\C按月合成2\\"
# output_folder = r"D:\\云量数据\\D按年合成平均值\\"
root_folder = r"C:\\云量数据\\季度实验\\"
output_folder = r"D:\\云量数据\\D每年逐个季度\\2017\\"
for subfolder in tqdm(os.listdir(root_folder)):
    subfolder_path = os.path.join(root_folder, subfolder)
    if os.path.isdir(subfolder_path):
        files = [f for f in os.listdir(subfolder_path) if f.endswith('.tif')]

        # 打开第一个 TIFF 文件，获取元数据信息
        first = os.path.join(subfolder_path, files[0])
        src_ds = gdal.Open(first)
        x_size = src_ds.RasterXSize
        y_size = src_ds.RasterYSize
        data_type = src_ds.GetRasterBand(1).DataType
        projection = src_ds.GetProjection()
        geotransform = src_ds.GetGeoTransform()

        # 创建输出文件
        output_file = os.path.join(output_folder, f"{subfolder}.tif")
        driver = gdal.GetDriverByName("GTiff")
        dst_ds = driver.Create(output_file, x_size, y_size, 1, gdal.GDT_Int16, options=["COMPRESS=DEFLATE"])
        dst_ds.SetProjection(projection)
        dst_ds.SetGeoTransform(geotransform)

        # 根据 x_size 和 y_size 计算分块大小
        x_block_size = x_size // 3
        y_block_size = y_size // 3
        # x_block_size = x_size
        # y_block_size = y_size
        # 分块读取 TIFF 文件并计算累积值
        for x_offset in range(0, x_size, x_block_size):
            for y_offset in range(0, y_size, y_block_size):
                block_width = min(x_block_size, x_size - x_offset)
                block_height = min(y_block_size, y_size - y_offset)

                # 初始化平均值数组
                sum_array = np.zeros((block_height, block_width), dtype=np.int16)
                count = 0

                # 遍历所有 TIFF 文件，计算平均值
                for file_name in files:
                    file_path = os.path.join(subfolder_path, file_name)

                    # 打开 TIFF 文件
                    src_ds = gdal.Open(file_path)

                    # 获取数组数据
                    array = src_ds.GetRasterBand(1).ReadAsArray(x_offset, y_offset, block_width, block_height)

                    # 计算累积值和像素数量
                    sum_array += array
                    count += 1

                # 计算平均值
                mean_array = (sum_array / count).astype(np.uint16)

                # 将数组数据写入输出文件
                out_band = dst_ds.GetRasterBand(1)
                out_band.WriteArray(mean_array.astype(np.int16), x_offset, y_offset)
                out_band=None
                mean_array=None
                sum_array=None

        # 释放资源
        dst_ds = None
