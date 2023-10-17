import gma
InFile = r'F:\公司\中粮\按照区域整理NDVI\未整理\原始NDVI\辐射校正_正射校正_裁剪_融合_配准_NDVI_山西大同1'
CutLineFile = r'E:\公司\中粮项目\地块矢量_第三次\合并\合并矢量.shp'

# 定义裁剪结果路径并执行裁剪，并为边界外数据分配无数据值
OutFile = r'F:\公司\中粮\按照区域整理NDVI\未整理\重分类后的NDVI\裁剪后栅格.tif'
gma.rasp.Clip(InFile, OutFile, CutLineFile, OutNoData = 0)