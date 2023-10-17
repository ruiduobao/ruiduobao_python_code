import gma

PATH=r"F:\帮别人忙\待拼接"
OutFile="F:\帮别人忙\镶嵌结果\镶嵌结果2.tif"
InFiles =gma.osf.GetPath(PATH, EXT = '.tif')
gma.rasp.Mosaic(InFiles, OutFile, InNoData =0, OutNoData = None, OutFormat = 'GTiff')
gma.rasp.GenerateOVR(OutFile, Force = True)


