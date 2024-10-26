import numpy as np
import pandas as pd



# 避免同一疾病的不同名字的问题，手动获取数据库

# target_disease.xlsx  D1列为目标疾病的名字
# Mesh_ID.xlsx  disease列为目前疾病的名字，ID列为目标疾病的ID

# Mesh_ID.xlsx表  ID列 按照字符串从长到短排列  解决相同祖先取最大值的问题

print("开始读取数据")
# 读取数据
Mesh_ID = pd.read_excel('Mesh_ID.xlsx', header=0)
disease = Mesh_ID['disease'].tolist()#将disease列转化为列表
id = Mesh_ID['ID'].tolist()#将ID列转化为列表
print('disease',disease)
print('id',id)
a = pd.read_excel('target_disease.xlsx', header=0)
target_disease = a['D1'].tolist()
print('target_disease',target_disease)


# 初始化字典，有重复也没关系
# range(10)  0-9  ，不包含尾部   range(1,10)   1-9  指定开头
DV= a['D1'].tolist()
for i in range(len(target_disease)):
    DV[i] = {}
print(DV)

print("开始计算每个病的DV")

for j in range(len(target_disease)):
    for i in range(len(disease)):
         if target_disease[j] == disease[i]:
                print(id[i],len(id[i]))
                if len(id[i]) > 3:
                    DV[j][id[i]] = 1  # 对列表中第i个空字典的id[i](key值)赋值1；
                    id[i] = id[i][:-4]  # 数组切片，对第i个元素从第一个开始到倒数第四个进行截取（取掉后面4位）
                    print('id[i]', id[i])
                    print('DV[j]', DV[j])
                    if len(id[i]) > 3:
                        DV[j][id[i]] = round(1 * 0.5, 5)  # round(number,num_digits)number：需要四舍五入的数;digits：需要小数点后保留的位数；
                        id[i] = id[i][:-4]  # 数组切片，从第一个开始到倒数第四个进行截取
                        print('DV[j]', DV[j])
                        if len(id[i]) > 3:
                            DV[j][id[i]] = round(1 * 0.5 * 0.5, 5)
                            id[i] = id[i][:-4]
                            print(DV[j])
                            if len(id[i]) > 3:
                                DV[j][id[i]] = round(1 * 0.5 * 0.5 * 0.5, 5)
                                id[i] = id[i][:-4]
                                print(DV[j])
                                if len(id[i]) > 3:
                                    DV[j][id[i]] = round(1 * 0.5 * 0.5 * 0.5 * 0.5, 5)
                                    id[i] = id[i][:-4]
                                    print(DV[j])
                                    if len(id[i]) > 3:
                                        DV[j][id[i]] = round(1 * 0.5 * 0.5 * 0.5 * 0.5 * 0.5, 5)
                                        id[i] = id[i][:-4]
                                        print(DV[j])
                                        if len(id[i]) > 3:
                                            DV[j][id[i]] = round(1 * 0.5 * 0.5 * 0.5 * 0.5 * 0.5 * 0.5, 5)
                                            id[i] = id[i][:-4]
                                            print(DV[j])
                                            if len(id[i]) > 3:
                                                DV[j][id[i]] = round(1 * 0.5 * 0.5 * 0.5 * 0.5 * 0.5 * 0.5 * 0.5, 5)
                                                id[i] = id[i][:-4]
                                                print(DV[j])
                                            else:
                                                DV[j][id[i][:3]] = round(1 * 0.5 * 0.5 * 0.5 * 0.5 * 0.5 * 0.5 * 0.5, 5)
                                                print(DV[j])
                                        else:
                                            DV[j][id[i][:3]] = round(1 * 0.5 * 0.5 * 0.5 * 0.5 * 0.5 * 0.5, 5)
                                            print(DV[j])
                                    else:
                                        DV[j][id[i][:3]] = round(1 * 0.5 * 0.5 * 0.5 * 0.5 * 0.5, 5)
                                        print(DV[j])
                                else:
                                    DV[j][id[i][:3]] = round(1 * 0.5 * 0.5 * 0.5 * 0.5, 5)
                                    print(DV[j])
                            else:
                                DV[j][id[i][:3]] = round(1 * 0.5 * 0.5 * 0.5, 5)
                                print(DV[j])
                        else:
                            DV[j][id[i][:3]] = round(1 * 0.5 * 0.5, 5)
                            print(DV[j])
                    else:
                        DV[j][id[i][:3]] = round(1 * 0.5, 5)
                        print(DV[j])
                else:
                      DV[j][id[i][:3]] = 1  # 对列表中第i个空字典的id[i](key值)截取前三位进行 赋值1；
                      print(DV[j])
print('DV:',DV)#最终结果
'''
print("合并相同的病不同ID的DV")

# 合并相同的病不同ID的DV

target_disease = a['D1'].tolist()


# 这个name用来判断
disease_name = Mesh_ID['disease'].tolist()
target_disease_name = a['D1'].tolist()

for i in range(len(target_disease)):
    target_disease[i] = {}
    for j in range(len(disease_name)):
        if target_disease_name[i] == disease_name[j]:
            for key in disease[j].keys():
                if key not in target_disease[i].keys() or target_disease[i][key]<disease[j][key]:
                    target_disease[i][key]=disease[j][key]
        #另一种实现方式，稍微复杂
            # if  len(unique_disease[i])!=0 and len(unique_disease[i].keys() & disease[j].keys()) != 0:
            #     for key in unique_disease[i].keys() & disease[j].keys():#输出键相同的一个集合
            #         if unique_disease[i][key] < disease[j][key]:
            #             unique_disease[i][key] = disease[j][key]
            #     for key1 in disease[j].keys() - unique_disease[i].keys():#判断键不同的情况，也需要添加进去
            #         unique_disease[i][key1] = disease[j][key1]
            # else:
            #     unique_disease[i].update(disease[j])
            #存在更新不是最大值的问题，已解决
            #用update更新字典，会有两种情况：有相同的键时：会使用最新的字典dict2中该key对应的value值。有新的键时：会直接把字典dict2中的key、value加入到dict1中。
        #print('unique_disease[i]',unique_disease[i])
print('222222',target_disease)
print(len(target_disease))
'''

DMS = np.zeros([len(DV), len(DV)])#np.zeros(n,m):创建n行m列的全0矩阵

print("计算相似度")

#求每个疾病语义值为1的个数
count1 = []
for i in range(len(DV)):
    count=0
    for m,n in DV[i].items():
        if n==1:
            count += 1
    count1.append(count)
print('count1',count1)


for m in range(len(DV)):
    for n in range(len(DV)):

        numerator=0
        for k, v in DV[m].items():   #k,v循环DV[m].items()    (k,v)对应（键，值）
            if k in DV[n].keys():
                numerator += v + DV[n].get(k)#利用get()函数操作时当字典中不存在输入的键时会返回一个None，这样程序运行时就不会出异常
        print('numerator',numerator)



        #denominator1 = sum(unique_disease[m].values())  + sum(unique_disease[n].values())
        denominator = sum(DV[m].values())-(count1[m]-1) +\
                      sum(DV[n].values())-(count1[n]-1)#疾病语义相似性的分母，存在多个1相加的问题，已解决
        #print('denominator1',denominator1)
        print('denominator',denominator)

        if m==n:#如果不加这句代码，对角线元素可能大于1
            DMS[m, n] = 1
        else:
            DMS[m, n] = round(numerator/denominator, 5)#给矩阵赋值



print(DMS)
print("保存结果")

# 保存结果

np.save('DMS.npy',DMS)

result = pd.DataFrame(DMS)
result.to_excel('DMS.xlsx',header=0,index=0)
