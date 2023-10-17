import os
import arcpy
from arcpy.sa import *
import gma


# 设置输入文件夹和输出文件夹
input_folder = "D:\\keshan\\求年平均"
output_folder = "D:\\keshan\\求年平均结果33"

# 获取输入文件夹中的所有子文件夹
subfolders = [os.path.join(input_folder, d) for d in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, d))]

for subfolder in subfolders:
    print(subfolder)
    
    # 获取当前子文件夹中的所有 TIFF 文件
    input_files = [os.path.join(subfolder, f) for f in os.listdir(subfolder) if f.endswith('.tif')]
    print(input_files)
    # 将所有 TIFF 文件转换为 RasterLayer 对象列表
    input_rasters = [arcpy.Raster(file) for file in input_files]

    # # 计算输入影像的平均值
    outCellStats = CellStatistics(input_rasters, "MEAN", "DATA")

    # 创建相应的输出子文件夹
    output_subfolder = os.path.join(output_folder, os.path.basename(subfolder))
    os.makedirs(output_subfolder, exist_ok=True)

    # 输出结果为 16 位整数类型的 TIFF 文件
    output_file = os.path.join(output_subfolder, f"{os.path.basename(subfolder)}_mean.tif")
    print(output_file)
    
    outCellStats.save(output_file)

    # 修改输出 TIFF 文件的像素类型为 16 位整数
    arcpy.management.CopyRaster(
        in_raster=output_file,
        out_rasterdataset=os.path.join(output_subfolder, f"{os.path.basename(subfolder)}_mean_int16.tif"),
        pixel_type="16_BIT_UNSIGNED",

    )

    # 删除临时文件
    arcpy.management.Delete(output_file)
   