def detect_file_format(filepath):
    # 尝试使用h5py读取文件
    try:
        import h5py
        with h5py.File(filepath, 'r'):
            return "HDF5"
    except Exception as e:
        pass

    # 尝试使用GDAL读取文件
    try:
        from osgeo import gdal
        ds = gdal.Open(filepath)
        if ds is not None and "HDF4" in ds.GetDriver().ShortName:
            return "HDF4"
    except Exception as e:
        pass

    # 尝试使用netCDF4读取文件
    try:
        import netCDF4
        with netCDF4.Dataset(filepath, 'r'):
            return "NetCDF"
    except Exception as e:
        pass

    # 未能确定文件类型
    return None


INPUT_HDF="D:\帮别人忙\GPP\GPP\shishi.hdf"
file_format = detect_file_format(INPUT_HDF)
if file_format:
    print(f"The file is in {file_format} format.")
else:
    print
