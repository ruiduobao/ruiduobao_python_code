import os
import gma
from tqdm import tqdm

PathA=r"F:\哥白尼DEM\分省"

tif_paths=gma.osf.GetPath(PathA, EXT = '.tif')
print(tif_paths)
for path in tqdm(tif_paths):
    gma.rasp.GenerateOVR(path, Force=True)