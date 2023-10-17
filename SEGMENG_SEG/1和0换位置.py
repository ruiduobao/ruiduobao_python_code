from osgeo import gdal
import numpy as np
from tqdm import tqdm

# 读取栅格数据
dataset = gdal.Open('input.tif', gdal.GA_ReadOnly)

# 读取所有的栅格数据为numpy数组
band = dataset.GetRasterBand(1)
array = band.ReadAsArray()

# 创建一个新的栅格数据集，数据类型为无符号整型8，压缩选项为LZW
output_dataset = gdal.GetDriverByName('GTiff').Create('output2.tif', band.XSize, band.YSize, 1, gdal.GDT_Byte,
                                                       options=['COMPRESS=LZW'])
output_dataset.SetGeoTransform(dataset.GetGeoTransform())
output_dataset.SetProjection(dataset.GetProjection())
output_band = output_dataset.GetRasterBand(1)

# 用numpy.where来更改值，添加tqdm显示进度
for i in tqdm(range(array.shape[0])):
    row = array[i, :]
    row = np.where(row == 1, -9999, row)  # 先把1改为-9999
    row = np.where(row == 2, 1, row)  # 然后把2改为1
    row = np.where(row == -9999, 2, row)  # 最后把-9999（原来为1的值）改为2
    output_band.WriteArray(row[np.newaxis, :], 0, i)  # 将一维数组转换为二维数组

output_band.FlushCache()
output_dataset = None
