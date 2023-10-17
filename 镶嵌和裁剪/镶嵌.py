import gma

PATH=r"F:\帮别人忙\待拼接"
OutFile="F:\哥白尼DEM\全国DEM数据\全国哥白尼DEM数据.tif"
InFiles =gma.osf.GetPath(PATH, EXT = '.tif')
gma.rasp.Mosaic(InFiles, OutFile, InNoData =0, OutNoData = None, OutFormat = 'GTiff')
gma.rasp.GenerateOVR(OutFile, Force = True)


