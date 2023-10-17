import pygrib
from osgeo import gdal
from osgeo import osr
import numpy as np

# 打开grib文件
grbs = pygrib.open('20230731180000-90h-scwv-fc.grib2')

# 选择要处理的数据
grb = grbs.select()[0]

# 获取数据和元信息
data = grb.values
lat, lon = grb.latlons()

# 创建GeoTiff
driver = gdal.GetDriverByName("GTiff")
dst_ds = driver.Create('output.tif', data.shape[1], data.shape[0], 1, gdal.GDT_Float32)

# 设置GeoTiff元信息
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)  # 这是WGS84的代码
dst_ds.SetProjection(srs.ExportToWkt())

# 计算GeoTransform
xmin, ymin, xmax, ymax = [lon.min(), lat.min(), lon.max(), lat.max()]
xres = (xmax - xmin) / float(data.shape[1])
yres = (ymax - ymin) / float(data.shape[0])
geotransform = (xmin, xres, 0, ymax, 0, -yres)
dst_ds.SetGeoTransform(geotransform)

# 写入数据
dst_ds.GetRasterBand(1).WriteArray(data)

# 释放资源
dst_ds = None
