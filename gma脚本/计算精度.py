import numpy as np
from osgeo import gdal
import pandas as pd

# 读取tif文件
def read_tif(file_path):
    dataset = gdal.Open(file_path)
    return dataset.GetRasterBand(1).ReadAsArray()

# 计算混淆矩阵
def confusion_matrix(y_true, y_pred, labels):
    num_labels = len(labels)
    mtx = np.zeros((num_labels, num_labels))
    for i in range(num_labels):
        for j in range(num_labels):
            mtx[i,j] = np.sum((y_true == labels[i]) & (y_pred == labels[j]))
    return mtx

# 计算每个类别的精度
def compute_accuracy_per_class(confusion_mtx):
    return np.diag(confusion_mtx) / confusion_mtx.sum(axis=1)

# 计算 kappa 系数
def compute_kappa(confusion_mtx):
    n = np.sum(confusion_mtx)
    sum_po = np.sum(np.diag(confusion_mtx))
    sum_pe = sum(np.sum(confusion_mtx, axis=0) * np.sum(confusion_mtx, axis=1)) / n**2
    return (sum_po / n - sum_pe) / (1 - sum_pe)

# 读取真实地物和预测地物tif
truth_tif = read_tif('E:\公司\中蒙项目_2023_7_20\精度评价\分类结果.tif')
prediction_tif = read_tif('E:\公司\中蒙项目_2023_7_20\精度评价\真实结果.tif')

# 确保两个tif的形状相同
assert truth_tif.shape == prediction_tif.shape, "Shapes of tif files must match."

# 计算混淆矩阵
confusion_mtx = confusion_matrix(truth_tif.flatten(), prediction_tif.flatten(), labels=[0, 1, 2])

# 计算每个类别的精度
class_accuracy = compute_accuracy_per_class(confusion_mtx)

# 计算kappa系数
kappa = compute_kappa(confusion_mtx)

# 创建数据框保存结果
df = pd.DataFrame({'class': ['other', 'grassland', 'cultivated_land'], 'accuracy': class_accuracy})
df.loc[3] = ['kappa', kappa]

# 保存为csv
df.to_csv('accuracy_and_kappa.csv', index=False)
