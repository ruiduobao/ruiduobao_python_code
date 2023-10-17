import pygrib
import numpy as np
from osgeo import gdal, osr, gdal_array


# 打开文本文件以写入数据



def grib_to_tiff(file_path, output_dir):
    grbs = pygrib.open(file_path)

    for grb in grbs:
        with open('output.txt', 'w') as f:
            f.write(f'{grb.name}: {grb.units}\n')

        data = grb.values
        lat, lon = grb.latlons()

        # 获得数据的维度
        x_size = len(lon[0])
        y_size = len(lat[:, 0])

        # 创建GeoTiff文件
        driver = gdal.GetDriverByName('GTiff')
        parameter_name = grb.name.replace(" ", "_")  # 用下划线替换参数名中的空格

        # 从原始文件名中提取步长信息
        time_step = file_path.split('-')[1]

        output_file = output_dir + '/' + time_step + '-' + parameter_name + '.tif'  # 将步长信息添加到输出文件名中
        ds = driver.Create(output_file, x_size, y_size, 1, gdal.GDT_Float32)

        # 设置GeoTiff的坐标系和变换信息
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326)  # WGS84坐标系
        ds.SetProjection(srs.ExportToWkt())
        gt = [lon.min(), (lon.max()-lon.min())/x_size, 0, lat.max(), 0, (lat.min()-lat.max())/y_size]
        ds.SetGeoTransform(gt)

        # 将数据写入GeoTiff
        ds.GetRasterBand(1).WriteArray(data)
        ds.FlushCache()

    print(f"{file_path} has been converted to GeoTiff files and saved in {output_dir}")

# 使用函数
grib_to_tiff("E:\个人\博客\天气预报数据\原始\\20230731180000-84h-scda-fc.grib2","E:\个人\博客\天气预报数据\分解后")
