from osgeo import gdal
import numpy as np

# 读取TIF文件
input_path = r"F:\公司\中粮\未上传到系统\HEILONGJIANG_DAQIN_SENTINEL_0819_dikuai12\中间数据\裁剪NDVI.tif"
output_path =r"F:\公司\中粮\未上传到系统\HEILONGJIANG_DAQIN_SENTINEL_0819_dikuai12\中间数据\裁剪NDVI_OUTPUT.tif"

def covert_0_to1(input_path,output_path):
    dataset = gdal.Open(input_path)
    if not dataset:
        raise Exception("Could not open input dataset")

    # 获取影像的基本信息
    rows, cols = dataset.RasterYSize, dataset.RasterXSize
    bands = dataset.RasterCount

    # 确保输入影像只有一个波段
    if bands != 1:
        raise Exception("Input dataset must have only one band")

    # 创建输出文件
    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(output_path, cols, rows, bands, gdal.GDT_Float32)  # 将数据类型设置为Float32
    out_ds.SetProjection(dataset.GetProjection())
    out_ds.SetGeoTransform(dataset.GetGeoTransform())

    # 读取单个波段的数据
    band = dataset.GetRasterBand(1)
    data = band.ReadAsArray()

    # 将0值设置为nodata
    nodata_value = -3.4028235e+38  # Float32的nodata值，可以根据需要更改
    data[data == 0] = nodata_value

    # 将处理后的数据写入输出文件，并设置nodata值
    out_band = out_ds.GetRasterBand(1)
    out_band.WriteArray(data)
    out_band.SetNoDataValue(nodata_value)
    out_band.FlushCache()

    # 关闭文件
    dataset = None
    out_ds = None