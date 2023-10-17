from osgeo import ogr

# 输入矢量文件路径
input_shapefile = r"E:\个人\博客\锐多宝矢量\2023年2月12日版 - 副本\2013年\2013年县级\2013年县 - 副本.shp"
# 输出矢量文件路径
output_shapefile = r"E:\个人\博客\锐多宝矢量\2023年2月12日版 - 副本\2013年\2013年县级\2013年县_gdal4.shp"

from osgeo import ogr

# 输入矢量文件路径
input_shapefile = "input.shp"
# 输出矢量文件路径
output_shapefile = "output.shp"

# 打开输入矢量数据集
input_ds = ogr.Open(input_shapefile, 0)
if input_ds is None:
    print("无法打开输入数据集")
    exit(1)

# 获取输入图层
input_layer = input_ds.GetLayer()

# 获取输入图层的坐标参考系统信息
spatial_ref = input_layer.GetSpatialRef()

# 创建输出矢量文件
driver = ogr.GetDriverByName("ESRI Shapefile")
output_ds = driver.CreateDataSource(output_shapefile)
output_layer = output_ds.CreateLayer(input_layer.GetName(), geom_type=input_layer.GetGeomType(), srs=spatial_ref)

# 创建新的字符串字段并设置长度为254
field_defn = ogr.FieldDefn("new_string_field", ogr.OFTString)
field_defn.SetWidth(254)
output_layer.CreateField(field_defn)

# 复制原始字段结构到输出图层
for i in range(input_layer.GetLayerDefn().GetFieldCount()):
    field_defn = input_layer.GetLayerDefn().GetFieldDefn(i)
    # 使用UTF-8编码将字段名转换为字符串
    field_name = field_defn.GetNameRef().encode('utf-8').decode('utf-8')
    output_layer.CreateField(ogr.FieldDefn(field_name, ogr.OFTString))

# 遍历要素并将属性字段值转换为字符串
for feature in input_layer:
    new_feature = ogr.Feature(output_layer.GetLayerDefn())
    for i in range(output_layer.GetLayerDefn().GetFieldCount()):
        field_name = output_layer.GetLayerDefn().GetFieldDefn(i).GetName()
        if field_name == "new_string_field":
            # 使用UTF-8编码将属性值转换为字符串
            new_value = str(feature.GetField(i)).encode('utf-8').decode('utf-8')
            new_feature.SetField("new_string_field", new_value)
        else:
            new_feature.SetField(field_name, feature.GetField(i))
    new_feature.SetGeometry(feature.GetGeometryRef())
    output_layer.CreateFeature(new_feature)

# 清理资源
input_ds = None
output_ds = None
