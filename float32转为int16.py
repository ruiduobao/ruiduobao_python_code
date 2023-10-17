

import arcpy
from arcpy.sa import Raster, Con, RoundDown, RoundUp

# # 输入浮点数栅格文件路径
# input_raster = "C:\\云量数据\\C按年合成\\2018.tif"

# # 输出整数栅格文件路径
# output_raster = "D:\\云量数据\\D按年合成平均值\\2018.tif"
# 输入浮点数栅格文件路径
input_raster = "D:\\云量数据\\C按年合成_shiyan\\2018\\2018_mean.tif"

# 输出整数栅格文件路径
output_raster = "D:\\云量数据\\C按年合成_shiyan\\2018\\2018.tif"
# 将浮点数栅格乘以一个比例因子，以保留所需的小数位数
# 如果不需要保留小数位，将scale_factor设置为1
scale_factor = 1

arcpy.AddMessage("读取输入浮点数栅格...")
# 读取输入浮点数栅格
in_raster = Raster(input_raster)

arcpy.AddMessage("按比例因子缩放并进行四舍五入...")
# 按比例因子缩放
scaled_raster = in_raster * scale_factor

# 四舍五入
rounded_raster = Con(scaled_raster - RoundDown(scaled_raster) < 0.5, RoundDown(scaled_raster), RoundUp(scaled_raster))

arcpy.AddMessage("将缩放后的浮点数栅格转换为16位有符号整数（int16）并使用LZW压缩...")
# 将缩放后的浮点数栅格转换为16位有符号整数（int16）并使用LZW压缩
arcpy.management.CopyRaster(rounded_raster, output_raster, pixel_type="16_BIT_SIGNED", format="TIFF", transform="NONE", build_multidimensional_transpose="NO_TRANSPOSE")

arcpy.AddMessage("完成!")
