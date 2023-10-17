import gma

InFile=r""

Aspect_OutFile=r""
gma.raa.DEM.Aspect(InFile, Aspect_OutFile, OutFormat = 'GTiff', ComputeEdges = True, Band = 1, ZevenbergenThorne = False, Trigonometric = False, ZeroForFlat = False)
gma.rasp.GenerateOVR(Aspect_OutFile, Force = True)

HillShade_OutFile=r""
gma.raa.DEM.HillShade(InFile, HillShade_OutFile, OutFormat = 'GTiff', ComputeEdges = True, Band = 1, ZFactor = 1.0, Scale = 1.0, Azimuth = 315.0, Altitude = 45.0, Combined = False, ZevenbergenThorne = False)
gma.rasp.GenerateOVR(HillShade_OutFile, Force = True)

Roughness_OutFile=r""
gma.raa.DEM.Roughness(InFile, Roughness_OutFile, OutFormat = 'GTiff', ComputeEdges = True, Band = 1)
gma.rasp.GenerateOVR(Roughness_OutFile, Force = True)

Slope_OutFile=""
gma.raa.DEM.Slope(InFile, Slope_OutFile, OutFormat = 'GTiff', ComputeEdges = True, Band = 1, Scale = 1.0, UseDegree = True, ZevenbergenThorne = False)
gma.rasp.GenerateOVR(Slope_OutFile, Force = True)

TPI_OutFile=r""
gma.raa.DEM.TPI(InFile, TPI_OutFile, OutFormat = 'GTiff', ComputeEdges = True, Band = 1)
gma.rasp.GenerateOVR(TPI_OutFile, Force = True)