from osgeo import gdal
import numpy as np


# 打开输入 TIFF 文件
input_file = r'F:\公司\中粮\未上传到系统\JL1KF01A_PMS06_20230806095925_200183754_101_0009_001_L1（鹤岗234）（朱浩）\中间数据\设为nodata.tif'
output_file =r'F:\公司\中粮\未上传到系统\JL1KF01A_PMS06_20230806095925_200183754_101_0009_001_L1（鹤岗234）（朱浩）\中间数据\设为nodata2.tif'

dataset = gdal.Open(input_file, gdal.GA_ReadOnly)
if not dataset:
    raise Exception('Failed to open input TIFF file.')

# 获取 nodata 值和波段数
nodata = dataset.GetRasterBand(1).GetNoDataValue()
bands = dataset.RasterCount

# 创建一个与输入文件大小和数据类型相同的数组，用于保存修改后的数据
new_data = [dataset.GetRasterBand(i + 1).ReadAsArray() for i in range(bands)]

# 查找像素值为 [8, 1, nodata, -60] 的位置
mask = (new_data[0] == 1) & (new_data[1] == 1) & (new_data[2] == 1) & (new_data[3] == 1)

# 将这些位置上的所有波段像素值设置为 nodata
for band_data in new_data:
    band_data[mask] = nodata

# # 对于不满足 [8, 1, nodata, -60] 的像素，如果某个波段的值为 nodata 则改为 1
# inverse_mask = np.logical_not(mask)
# for band_data in new_data:
#     band_data[(band_data == nodata) & inverse_mask] = 1

# 创建一个新的 TIFF 文件，并将修改后的数据写入其中
driver = gdal.GetDriverByName('GTiff')
out_dataset = driver.Create(output_file, dataset.RasterXSize, dataset.RasterYSize, bands, dataset.GetRasterBand(1).DataType)
out_dataset.SetGeoTransform(dataset.GetGeoTransform())
out_dataset.SetProjection(dataset.GetProjection())

# 写入数据
for i, band_data in enumerate(new_data, 1):
    out_band = out_dataset.GetRasterBand(i)
    out_band.WriteArray(band_data)
    out_band.SetNoDataValue(nodata)

# 关闭数据集
dataset = None
out_dataset = None