import h5py
from osgeo import gdal, osr


def hdf_to_geotiff(hdf_file, output_tiff):
    # 使用h5py打开HDF文件
    with h5py.File(hdf_file, 'r') as ds:
        # 获取第一个数据集名称
        dataset_name = list(ds.keys())[0]
        var_data = ds[dataset_name][:]

        # 获取数据的形状（维度）
        nlat, nlon = var_data.shape

        # 假设HDF中有名为'lat'和'lon'的数据集来获取经纬度信息
        # 注意：确保您的HDF文件包含这些数据集
        lats = ds['lat'][:]
        lons = ds['lon'][:]

        # 创建一个GeoTIFF数据集
        driver = gdal.GetDriverByName('GTiff')
        out_ds = driver.Create(output_tiff, nlon, nlat, 1, gdal.GDT_Float32)

        # 设置地理变换
        geotransform = (lons.min(), (lons.max() - lons.min()) / nlon, 0,
                        lats.max(), 0, (lats.min() - lats.max()) / nlat)
        out_ds.SetGeoTransform(geotransform)

        # 设置投影信息（WGS84）
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326)  # WGS84 EPSG
        out_ds.SetProjection(srs.ExportToWkt())

        # 写入数据
        out_band = out_ds.GetRasterBand(1)
        out_band.WriteArray(var_data)
        out_band.FlushCache()


# 使用函数进行转换
INPUT_HDF="D:\帮别人忙\GPP\GPP\shishi.hdf"
hdf_to_geotiff(INPUT_HDF, 'output.tif')

