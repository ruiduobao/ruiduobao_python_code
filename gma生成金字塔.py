import  gma
from tqdm import tqdm

PATH=r"E:\cloud\output"
paths=gma.osf.GetPath(PATH, EXT = '.tif')
print(paths)
for path in tqdm(paths):
    gma.rasp.GenerateOVR(path)