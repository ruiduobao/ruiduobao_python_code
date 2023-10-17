from osgeo import gdal
import numpy as np

# 打开tif文件
input_path="F:\公司\中粮\吉林一号\处理后的影像\JL1GF02A_PMS2_20230714092344_200175369_104_0004_001_L1\辐射定标_正射校正_融合\辐射定标_正射校正_融合_104_0004.dat"
output_path="F:\公司\中粮\吉林一号\处理后的影像\JL1GF02A_PMS2_20230714092344_200175369_104_0004_001_L1\辐射定标_正射校正_融合_RGB渲染\获取相关处理小于1结果.tif"

src_ds = gdal.Open(input_path)
band_count = src_ds.RasterCount

# 创建新的tif文件
driver = gdal.GetDriverByName('GTiff')
out_ds = driver.Create(output_path, src_ds.RasterXSize, src_ds.RasterYSize, band_count, gdal.GDT_Float32)

# 复制地理变换和投影
out_ds.SetGeoTransform(src_ds.GetGeoTransform())
out_ds.SetProjection(src_ds.GetProjection())

# 遍历每个波段进行处理
for b in range(band_count):
    src_band = src_ds.GetRasterBand(b + 1)

    # 读取数据为numpy数组
    src_array = src_band.ReadAsArray()

    # 值等于0加1
    # src_array[src_array == 0] += 1
    # 值小于1命为空
    src_array[src_array < 0.02] = np.nan

    # # 将数组的数据类型转换为uint16
    # src_array = src_array.astype(np.uint16)

    # 将处理后的数组写入新的tif文件
    out_band = out_ds.GetRasterBand(b + 1)
    out_band.WriteArray(src_array)

# 保存和关闭tif文件
out_ds.FlushCache()
out_ds = None
