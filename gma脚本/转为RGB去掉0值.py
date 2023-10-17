from osgeo import gdal
import numpy as np
def processrgb(rasterpath,outtif):
    maskpath = r"F:\公司\中粮\高分影像\E119N42_0703\辐射校正_正射校正_融合_裁剪小区域_地理配准_RGB可视化\辐射校正_正射校正_融合_裁剪小区域_地理配准_改变0值.tif"
    mask = gdal.Open(maskpath).ReadAsArray()

    dataset = gdal.Open(rasterpath)
    proj = dataset.GetProjection()
    gt = dataset.GetGeoTransform()
    cols, rows = dataset.RasterXSize, dataset.RasterYSize
    b1 = dataset.GetRasterBand(1).ReadAsArray()
    b2 = dataset.GetRasterBand(2).ReadAsArray()
    b3 = dataset.GetRasterBand(3).ReadAsArray()
    b1[np.where(b1 == 0)] = 1
    b2[np.where(b2 ==  0)] = 1
    b3[np.where(b3 ==  0)] = 1
    format = "GTiff"
    driver = gdal.GetDriverByName( format )
    dst_ds = driver.Create(outtif,cols, rows, 3, gdal.GDT_Byte)

    dst_ds.SetGeoTransform(gt)
    dst_ds.SetProjection(proj)
    outband1=dst_ds.GetRasterBand(1)
    outband1.SetNoDataValue(0)
    outband1.WriteArray(b1*mask)
    outband2=dst_ds.GetRasterBand(2)
    outband2.SetNoDataValue(0)
    outband2.WriteArray(b2*mask)
    outband3=dst_ds.GetRasterBand(3)
    outband3.SetNoDataValue(0)
    outband3.WriteArray(b3*mask)
    dst_ds = None
processrgb("F:\公司\中粮\高分影像\E119N42_0703\辐射校正_正射校正_融合_裁剪小区域_地理配准_RGB可视化\辐射校正_正射校正_融合_裁剪小区域_地理配准_改变0值.tif","F:\公司\中粮\高分影像\E119N42_0703\辐射校正_正射校正_融合_裁剪小区域_地理配准_RGB可视化\JIEGUO.tif",)