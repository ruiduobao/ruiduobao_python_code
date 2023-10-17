from osgeo import gdal
import numpy as np
from tqdm import tqdm

# 打开图像
dataset = gdal.Open('E:\下载\\101_0019.tif', gdal.GA_ReadOnly)
bands = dataset.RasterCount

# 创建新的 GeoTIFF 文件，设置 LZW 压缩
driver = gdal.GetDriverByName('GTiff')
options = ['COMPRESS=LZW']
out_dataset = driver.Create('101_0019.tif', dataset.RasterXSize, dataset.RasterYSize, bands, gdal.GDT_Byte, options=options)

# 复制地理变换参数和投影信息
out_dataset.SetGeoTransform(dataset.GetGeoTransform())
out_dataset.SetProjection(dataset.GetProjection())

# 处理每个波段
for b in tqdm(range(bands), desc="Processing bands", unit="band"):
    band = dataset.GetRasterBand(b + 1)

    # 读取图像数据
    data = band.ReadAsArray().astype(np.float64)

    # 计算均值和标准差
    mean = np.mean(data)
    std = np.std(data)

    # 执行拉伸
    data[data < mean - 2*std] = mean - 2*std
    data[data > mean + 2*std] = mean + 2*std

    # 将拉伸后的数据重新映射到 0-255
    data = ((data - np.min(data)) / (np.max(data) - np.min(data)) * 255).astype(np.uint8)

    # 将拉伸后的数据写入新的 GeoTIFF 文件
    out_band = out_dataset.GetRasterBand(b + 1)
    out_band.WriteArray(data)

# 保存并关闭文件
out_dataset.FlushCache()
out_dataset = None
