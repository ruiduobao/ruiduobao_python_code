from osgeo import gdal, gdal_array
import numpy as np
import gma

PATH=r"F:\公司\中粮\未上传到系统\GF01_PM2_055246_20230727_MY0A2_01_067_L1A_01\辐射校正_大气校正_裁剪_正射_配准_融合_NDVI\ndvi结果.tif"
OUT_PATH=r"F:\公司\中粮\未上传到系统\GF01_PM2_055246_20230727_MY0A2_01_067_L1A_01\提交数据\NEIMENGGU_CHIFENG_GF_NDVI_0727_DIKUAI3.tif"


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

# 将所有大于0.6的像素设置为分类11
output_array[(ndvi_array > 0.6) & (ndvi_array != nodata_orig)] = 10

# 创建新的tif文件，以保存分类结果，使用LZW压缩
driver = gdal.GetDriverByName('GTiff')
output_dataset = driver.Create(OUT_PATH, ndvi_dataset.RasterXSize, ndvi_dataset.RasterYSize, 1, gdal.GDT_Byte, options=["COMPRESS=LZW"])

# 写入数据
output_dataset.GetRasterBand(1).WriteArray(output_array)
output_dataset.GetRasterBand(1).SetNoDataValue(nodata_new)

# 将地理变换和投影从原始数据集复制到新数据集
output_dataset.SetGeoTransform(ndvi_dataset.GetGeoTransform())
output_dataset.SetProjection(ndvi_dataset.GetProjectionRef())

# 清理关闭数据集
ndvi_dataset = None
output_dataset = None

## 待更新的色彩映射表
ColorTable = {
10:(36,247,0,255),
9:(78,247,0,255),
8:(115,247,0,255),
7:(148,247,0,255),
6:(186,247,0,255),
5:(214,247,0,255),
4:(245,245,0,255),
3:(250,208,79,255),
2:(252,177,0,255),
1:(252,139,0,255),
}
## 将定义的色彩映射表更新到 副本
gma.rasp.AddColorTable(OUT_PATH,ColorTable = ColorTable)