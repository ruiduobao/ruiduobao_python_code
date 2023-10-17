import gma

PathA=r"F:\哥白尼2\实验"
OUTPUT_PATH=r"F:\哥白尼2\转格式\\"
tif_paths=gma.osf.GetPath(PathA, EXT = '.tif')
print(tif_paths)
for tif_path in tif_paths:
    tif_name=tif_path.split("\\")[-1]
    print(tif_name)
    OutFile=OUTPUT_PATH+tif_name
    gma.rasp.ChangeDataType(tif_path, OutFile, 'Int16')
# print('输入栅格数据类型：', gma.Open(InFile).DataType)
# gma.rasp.ChangeDataType(InFile, OutFile, 'Float32')
# print('输出栅格数据类型：', gma.Open(OutFile).DataType)

