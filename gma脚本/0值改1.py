from osgeo import gdal
import numpy as np

# 读取TIF文件
input_path =r"F:\公司\中粮\未上传到系统\DP09_PMS_20230720142830_200177583_102_0006_001_L1（鹤岗3）\辐射定标_大气校正_正射校正\多光谱正射.tif"
output_path =r"F:\公司\中粮\未上传到系统\DP09_PMS_20230720142830_200177583_102_0006_001_L1（鹤岗3）\辐射定标_大气校正_正射校正\去除0值的多光谱.tif"

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

# 创建一个与输入影像同大小的bool数组，所有值初始化为True
nodata_mask = np.ones((rows, cols), dtype=bool)

# 处理每个波段
for i in range(1, bands + 1):
    band = dataset.GetRasterBand(i)
    data = band.ReadAsArray()
    data[data == 0] = 1 # 将0值替换为1

    # 将处理后的数据写入输出文件
    out_band = out_ds.GetRasterBand(i)
    out_band.WriteArray(data)
    out_band.FlushCache()

    # 更新nodata_mask
    nodata_mask &= (data == 1)

# 将所有波段都为1的像素设置为NoData值
nodata_value = 0
for i in range(1, bands + 1):
    out_band = out_ds.GetRasterBand(i)
    out_band.SetNoDataValue(nodata_value)
    out_band.WriteArray(np.where(nodata_mask, nodata_value, out_band.ReadAsArray()))
    out_band.FlushCache()

# 关闭文件
dataset = None
out_ds = None