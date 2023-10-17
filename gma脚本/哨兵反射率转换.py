from osgeo import gdal
import numpy as np

# 打开tif文件
src_ds = gdal.Open("反射率.tif")
band_count = src_ds.RasterCount

# 创建新的tif文件
driver = gdal.GetDriverByName('GTiff')
out_ds = driver.Create('output.tif', src_ds.RasterXSize, src_ds.RasterYSize, band_count, gdal.GDT_UInt16)

# 复制地理变换和投影
out_ds.SetGeoTransform(src_ds.GetGeoTransform())
out_ds.SetProjection(src_ds.GetProjection())

# 遍历每个波段进行处理
for b in range(band_count):
    src_band = src_ds.GetRasterBand(b + 1)

    # 读取数据为numpy数组
    src_array = src_band.ReadAsArray()

    # 对数组进行操作（乘以10000）
    src_array = src_array * 10000

    # 将数组的数据类型转换为uint16
    src_array = src_array.astype(np.uint16)

    # 将处理后的数组写入新的tif文件
    out_band = out_ds.GetRasterBand(b + 1)
    out_band.WriteArray(src_array)

# 保存和关闭tif文件
out_ds.FlushCache()
out_ds = None
