# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 02:24:50 2023

@author: Administrator
"""

import arcpy

# 输入和输出栅格数据的路径
input_raster = "D:\\keshan\\求年平均结果33\\AA\\公众号遥感之家_2000年浙江省_温州市_文成县CLC30土地覆盖30米分辨率.tif"
output_raster = "D:\\keshan\\求年平均结果33\\AA\\AA_mean_int16DEFLATE222.tif"

# 将输入栅格数据的压缩方式从 LZW 改为 DEFLATE
arcpy.management.CopyRaster(
    in_raster=input_raster,
    out_rasterdataset=output_raster,
    config_keyword="DEFLATE"
)
