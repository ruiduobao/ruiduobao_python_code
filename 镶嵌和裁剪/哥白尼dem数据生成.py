import gma
from tqdm import tqdm

PathA=r"F:\哥白尼DEM\全国原始DEM数据(float32)"
OUTPUT_PATH=r"F:\哥白尼DEM\全国原始DEM数据(int16)\\"
tif_paths=gma.osf.GetPath(PathA, EXT = '.tif')
print(tif_paths)
for tif_path in tqdm(tif_paths):
    tif_name=tif_path.split("\\")[-1]
    print(tif_name)
    OutFile=OUTPUT_PATH+tif_name
    gma.rasp.ChangeDataType(tif_path, OutFile, 'Int16')

PATH=r"F:\哥白尼DEM\全国原始DEM数据(int16)"
DEM_OutFile="F:\哥白尼DEM\全国DEM数据\全国哥白尼DEM数据.tif"
InFiles =gma.osf.GetPath(PATH, EXT = '.tif')
gma.rasp.Mosaic(InFiles, DEM_OutFile, InNoData =0, OutNoData = None, OutFormat = 'GTiff')
gma.rasp.GenerateOVR(DEM_OutFile, Force = True)

Aspect_OutFile=r"F:\哥白尼DEM\全国坡向数据\全国哥白尼坡向数据.tif"
gma.raa.DEM.Aspect(DEM_OutFile, Aspect_OutFile, OutFormat = 'GTiff', ComputeEdges = True, Band = 1, ZevenbergenThorne = False, Trigonometric = False, ZeroForFlat = False)
gma.rasp.GenerateOVR(Aspect_OutFile, Force = True)

HillShade_OutFile=r"F:\哥白尼DEM\全国山体阴影数据\全国哥白尼山体阴影数据.tif"
gma.raa.DEM.HillShade(DEM_OutFile, HillShade_OutFile, OutFormat = 'GTiff', ComputeEdges = True, Band = 1, ZFactor = 1.0, Scale = 1.0, Azimuth = 315.0, Altitude = 45.0, Combined = False, ZevenbergenThorne = False)
gma.rasp.GenerateOVR(HillShade_OutFile, Force = True)

Roughness_OutFile=r"F:\哥白尼DEM\全国粗糙度数据\全国哥白尼粗糙度数据.tif"
gma.raa.DEM.Roughness(DEM_OutFile, Roughness_OutFile, OutFormat = 'GTiff', ComputeEdges = True, Band = 1)
gma.rasp.GenerateOVR(Roughness_OutFile, Force = True)

Slope_OutFile="F:\哥白尼DEM\全国坡度数据\全国哥白尼坡度数据.tif"
gma.raa.DEM.Slope(DEM_OutFile, Slope_OutFile, OutFormat = 'GTiff', ComputeEdges = True, Band = 1, Scale = 1.0, UseDegree = True, ZevenbergenThorne = False)
gma.rasp.GenerateOVR(Slope_OutFile, Force = True)

TPI_OutFile=r"F:\哥白尼DEM\全国地形指数数据\全国哥白尼地形指数数据.tif"
gma.raa.DEM.TPI(DEM_OutFile, TPI_OutFile, OutFormat = 'GTiff', ComputeEdges = True, Band = 1)
gma.rasp.GenerateOVR(TPI_OutFile, Force = True)
