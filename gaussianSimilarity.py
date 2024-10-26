import numpy as np
import pandas as pd
import math

# 读取数据

association_matrix = pd.read_excel('G:\\疾病与RNA\\数据预处理（未删减）\\数据清洗\\associationMatrix.xlsx', header=None, ).values

#n行 m列，每行表示一个rna和每个病是否有联系，每列表示一个病和各rna是否有联系，

# 计算disease之间的相似度

Dassociation_matrix = association_matrix.T

# 转置之后有100行，676列，每行一个disease

disease_similarity = np.zeros([association_matrix.shape[1], association_matrix.shape[1]])  # 100种病之间的相似度，初始化矩阵

width = 0

for m in range(association_matrix.shape[1]):
    width += np.sum(Dassociation_matrix[m]**2)**0.5  # 按定义用二阶范数计算width parameter

print(width)

# 计算association_matrix
count = 0
for m in range(association_matrix.shape[1]):
    for n in range(association_matrix.shape[1]):
        disease_similarity[m, n] = math.exp((np.sum((Dassociation_matrix[m] - Dassociation_matrix[n])**2)**0.5
                                        * width/association_matrix.shape[1]) * (-1))  # 计算不同行（disease）之间的二阶范数
        if disease_similarity[m, n] == 1:
            disease_similarity[m, n] = 0.8  # 这里是一个大问题，两个向量相同可以说它有一定相关度，可是计算出相关度等于1又不合理，只能定义一个值


# 保存结果
np.save('GIP_DS.npy',disease_similarity)
result = pd.DataFrame(disease_similarity)
result.to_excel('disease_GaussianSimilarity.xlsx',header=0,index=0)
# 注意，这样保存之后会多了一行一列行号序号，需要删除


# 计算circRNA之间的相似度


rna_similarity = np.zeros([association_matrix.shape[0], association_matrix.shape[0]])  # 676种circRNA之间的相似度，初始化矩阵

# 计算association_matrix

count = 0

for m in range(association_matrix.shape[0]):
    count += np.sum(association_matrix[m]**2)**0.5
for m in range(association_matrix.shape[0]):
    for n in range(association_matrix.shape[0]):
        rna_similarity[m, n] = math.exp((np.sum((association_matrix[m] - association_matrix[n])**2)**0.5
                                        * count/association_matrix.shape[0]) * (-1))
        if rna_similarity[m, n] == 1:
            rna_similarity[m, n] = 0.8  # 这里是一个大问题，两个向量相同可以说它有一定相关度，可是计算出相关度等于1又不合理，只能定义一个值


# 保存结果


np.save('GIP_RS.npy',rna_similarity)

result = pd.DataFrame(rna_similarity)
result.to_excel('rna_GaussianSimilarity.xlsx',header=0,index=0)

# 注意，这样保存之后会多了一行一列行号序号，需要删除




