from osgeo import gdal
import numpy as np

# 读取TIF文件
input_path = "F:\公司\中粮\未上传到系统\JL1GF02D_PMS1_20230802123403_200182244_101_0001_001_L1（鹤岗567）\地块8\裁剪结果\融合地块8裁剪结果.dat"
output_path = "F:\公司\中粮\未上传到系统\JL1GF02D_PMS1_20230802123403_200182244_101_0001_001_L1（鹤岗567）\地块8\裁剪结果\融合地块8裁剪结果_改nodata.dat"

dataset = gdal.Open(input_path)
if not dataset:
    raise Exception("Could not open input dataset")

# 获取影像的基本信息
rows, cols = dataset.RasterYSize, dataset.RasterXSize
bands = dataset.RasterCount

# 创建输出文件
driver = gdal.GetDriverByName("GTiff")
out_ds = driver.Create(output_path, cols, rows, bands, gdal.GDT_Int16)
out_ds.SetProjection(dataset.GetProjection())
out_ds.SetGeoTransform(dataset.GetGeoTransform())

# 创建一个数组来保存nodata计数
nodata_count = np.zeros((rows, cols), dtype=int)

# 计算每个像素的nodata计数
nodata_value = -32768  # int16的nodata值
for i in range(1, bands + 1):
    band = dataset.GetRasterBand(i)
    data = band.ReadAsArray()
    nodata_mask = (data == nodata_value)
    nodata_count += nodata_mask.astype(int)

# 处理每个波段
for i in range(1, bands + 1):
    band = dataset.GetRasterBand(i)
    data = band.ReadAsArray()

    # 将1到3个波段为nodata的像素值改为1
    mask = (nodata_count >= 1) & (nodata_count < 4)
    data[mask] = 1

    # 将处理后的数据写入输出文件
    out_band = out_ds.GetRasterBand(i)
    out_band.WriteArray(data)
    out_band.FlushCache()

# 关闭文件
dataset = None
out_ds = None
