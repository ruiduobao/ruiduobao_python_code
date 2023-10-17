from osgeo import gdal, gdal_array
import numpy as np

PATH="F:\公司\中粮\未上传到系统\GF1B_PMS_E113.2_N40.2_20230711_L1A1228323629(山西大同1)\辐射校正_正射校正_裁剪_融合_配准_NDVI\\ndvi裁剪数据.tif"
OUT_PATH="F:\公司\中粮\未上传到系统\GF1B_PMS_E113.2_N40.2_20230711_L1A1228323629(山西大同1)\辐射校正_正射校正_裁剪_融合_配准_NDVI\\NDVI_classified3.tif"

# 加载NDVI数据
ndvi_dataset = gdal.Open(PATH, gdal.GA_ReadOnly)

# 读取数据到numpy数组
ndvi_array = ndvi_dataset.ReadAsArray()

# 获取原始nodata值
nodata_orig = ndvi_dataset.GetRasterBand(1).GetNoDataValue()

# 设定新的nodata值
nodata_new = 255

# 重新分类的阈值
thresholds = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6]

# 初始化一个全为新nodata的数组，与NDVI数组形状相同，这将是我们的输出
output_array = np.full_like(ndvi_array, nodata_new, dtype=np.uint8)

# 对每个阈值进行循环
for i, threshold in enumerate(thresholds, start=1):
    output_array[(ndvi_array > threshold) & (ndvi_array != nodata_orig)] = i

# 创建新的tif文件，以保存分类结果
driver = gdal.GetDriverByName('GTiff')
output_dataset = driver.Create(OUT_PATH, ndvi_dataset.RasterXSize, ndvi_dataset.RasterYSize, 1, gdal.GDT_Byte)

# 写入数据
output_dataset.GetRasterBand(1).WriteArray(output_array)
output_dataset.GetRasterBand(1).SetNoDataValue(nodata_new)

# 将地理变换和投影从原始数据集复制到新数据集
output_dataset.SetGeoTransform(ndvi_dataset.GetGeoTransform())
output_dataset.SetProjection(ndvi_dataset.GetProjectionRef())

# 清理关闭数据集
ndvi_dataset = None
output_dataset = None
