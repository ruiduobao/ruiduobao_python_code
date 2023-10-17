from osgeo import gdal, gdal_array
import numpy as np
import gma
import tqdm
from covert0tonoadata import covert_0_to1

#在这里添加文件夹路径，文件夹内需要包含两个数据：NDVI的tif格式数据以及裁剪矢量的.shp数据
PATH=r"F:\公司\中粮\未上传到系统\HEILONGJIANG_DAQIN_SENTINEL_0826_dikuai12\中间数据"

TIF_CLIP_PATH=gma.osf.GetPath(PATH, EXT = '.tif')[0]

SHP_PATH=gma.osf.GetPath(PATH, EXT = '.shp')[0]
CAIJIAN_PATH=PATH+"\\"+"裁剪NDVI.tif"
PATH2=PATH+"\\"+"裁剪NDVI_OUTPUT.tif"
OUT_PATH=PATH+"\\"+"结果数据.tif"
OUT_PATH2=PATH+"\\"+"结果数据2.tif"

gma.rasp.Clip(TIF_CLIP_PATH, CAIJIAN_PATH, SHP_PATH)
covert_0_to1(CAIJIAN_PATH,PATH2)
# 加载NDVI数据

ndvi_dataset = gdal.Open(PATH2, gdal.GA_ReadOnly)

# 读取数据到numpy数组
ndvi_array = ndvi_dataset.ReadAsArray()

# 获取原始nodata值
nodata_orig = ndvi_dataset.GetRasterBand(1).GetNoDataValue()

# nodata_orig[data == 0] = nodata_value

# 设定新的nodata值
nodata_new = 255
# nodata_new = 0

# 重新分类的阈值
# thresholds = [0, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6]
thresholds = [0, 0.2, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.75]
# thresholds = [0, 0.1, 0.36, 0.59, 0.65, 0.75, 0.8, 0.85, 0.88, 0.92]
# #PLANET修改
# thresholds = [0, 0.2, 0.36, 0.59, 0.7, 0.76, 0.79, 0.82, 0.85, 0.9]
# thresholds = [0, 0.2, 0.36, 0.59, 0.7, 0.76, 0.79, 0.82, 0.9, 1.03]
# 初始化一个全为新nodata的数组，与NDVI数组形状相同，这将是我们的输出
output_array = np.full_like(ndvi_array, nodata_new, dtype=np.uint8)

# 对每个阈值进行循环
for i, threshold in enumerate(thresholds, start=1):
    output_array[(ndvi_array > threshold) & (ndvi_array != nodata_orig)] = i

# 将所有大于阈值的像素设置为分类11
output_array[(ndvi_array > thresholds[-1]) & (ndvi_array != nodata_orig)] = 10
output_array[(ndvi_array < thresholds[1]) & (ndvi_array != nodata_orig)] = 1
# 创建新的tif文件，以保存分类结果，使用LZW压缩
driver = gdal.GetDriverByName('GTiff')
output_dataset = driver.Create(OUT_PATH, ndvi_dataset.RasterXSize, ndvi_dataset.RasterYSize, 1, gdal.GDT_Byte, options=["COMPRESS=LZW"])

# 写入数据
output_dataset.GetRasterBand(1).WriteArray(output_array)
output_dataset.GetRasterBand(1).SetNoDataValue(nodata_new)

# 将地理变换和投影从原始数据集复制到新数据集
output_dataset.SetGeoTransform(ndvi_dataset.GetGeoTransform())
output_dataset.SetProjection(ndvi_dataset.GetProjectionRef())

# 清理关闭数据集
ndvi_dataset = None
output_dataset = None

## 待更新的色彩映射表
ColorTable = {
10:(36,247,0,255),
9:(78,247,0,255),
8:(115,247,0,255),
7:(148,247,0,255),
6:(186,247,0,255),
5:(214,247,0,255),
4:(245,245,0,255),
3:(250,208,79,255),
2:(252,177,0,255),
1:(252,139,0,255),
}

covert_0_to1(CAIJIAN_PATH,PATH2)
## 将定义的色彩映射表更新到 副本
gma.rasp.AddColorTable(OUT_PATH,ColorTable = ColorTable)