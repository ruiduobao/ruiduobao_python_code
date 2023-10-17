import pygrib

# 打开GRIB2文件
grbs = pygrib.open('E:\个人\博客\天气预报数据\\20230731180000-0h-scda-fc.grib2')

# 打开文本文件以写入数据
with open('output2.txt', 'w') as f:
    # 遍历所有GRIB2消息（每个消息对应一个气象要素）
    for grb in grbs:
        # 将要素的名字和单位写入文本文件
        f.write(f'{grb.name}: {grb.units}\n')