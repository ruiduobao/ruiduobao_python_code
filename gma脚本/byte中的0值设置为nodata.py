from osgeo import gdal


def set_nodata(input_tif, output_tif, nodata_value=0):
    # 打开输入的TIFF文件
    src_ds = gdal.Open(input_tif, gdal.GA_ReadOnly)

    # 使用gdal.Translate将0值设置为NoData
    out_ds = gdal.Translate(output_tif, src_ds, options=f"-a_nodata {nodata_value}")

    # 关闭数据集
    out_ds = None
    src_ds = None


# 使用函数
input_tif_path = 'path_to_input.tif'
output_tif_path = 'path_to_output.tif'
set_nodata(input_tif_path, output_tif_path)


