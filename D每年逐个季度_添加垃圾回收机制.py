import os
import numpy as np
from osgeo import gdal
from tqdm import tqdm
import gc

root_folder = r"C:\\云量数据\\季度实验\\"
output_folder = r"D:\\云量数据\\D每年逐个季度\\2017\\"
# root_folder = r"D:\\keshan\\gdal\\代求\\"
# output_folder = r"D:\\keshan\\gdal\\结果\\"
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
        dst_ds = driver.Create(output_file, x_size, y_size, 1, gdal.GDT_Int16, options=["COMPRESS=DEFLATE", "BIGTIFF=YES"])
        dst_ds.SetProjection(projection)
        dst_ds.SetGeoTransform(geotransform)

        # 计算分块大小
        x_block_size = x_size // 3
        y_block_size = y_size // 3

        # 遍历所有分块 TIFF 文件，计算平均值并将块写入输出文件
        for x_offset in range(0, x_size, x_block_size):
            for y_offset in range(0, y_size, y_block_size):
                # 计算当前块的实际大小
                block_width = min(x_block_size, x_size - x_offset)
                block_height = min(y_block_size, y_size - y_offset)

                # 创建内存映射数组 int32 的范围是65536，只适合6景以内的  如果是一年12景，需要用int64
                dtype = np.int32
                mmap_array = np.memmap('mmap.bin', dtype=dtype, mode='w+', shape=(block_height, block_width))

                # 遍历所有 TIFF 文件，将像素值逐个读取到内存映射数组中
                for file_name in files:
                    file_path = os.path.join(subfolder_path, file_name)

                    # 打开 TIFF 文件
                    src_ds = gdal.Open(file_path)

                    # 将分块的像素值读取到数组中
                    array = src_ds.GetRasterBand(1).ReadAsArray(x_offset, y_offset, block_width, block_height)

                    # 将数组中的像素值加到内存映射数组中
                    mmap_array += array

                    # 释放资源
                    src_ds = None

                # 计算平均值
                mean_array = (mmap_array / len(files)).astype(np.int16)

                # 将平均值数组写入输出文件
                out_band = dst_ds.GetRasterBand(1)
                out_band.WriteArray(mean_array, xoff=x_offset, yoff=y_offset)

                # 释放内存映射数组和垃圾回收
                mmap_array.flush()
                mmap_array._mmap.close()
                os.unlink('mmap.bin')
                del mmap_array, mean_array, out_band, array
                gc.collect()

        # 关闭输出文件
        dst_ds = None
