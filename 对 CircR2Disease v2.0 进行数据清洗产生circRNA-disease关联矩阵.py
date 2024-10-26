import pandas as pd
from pandas import DataFrame as df

'''
我们可以看到 “The circRNA-disease entries.xlsx” 表格统计中的“Species”一列中既有 human，还有 mouse，rat的数据统计，根据需求，我们就只需要human的数据统计。
那我们的一个思路就是只保留human字段所在的行。也可理解为第一步数据清洗。其处理的代码如下：

'''

#Code block 1

data = pd.read_excel('F:/daixie/data/dis_gene_association.xlsx')
data = df(data)
# 获得Human字段所在的行索引
index_human = data[(data.Species == 'Human')].index.tolist()
a = data.iloc[index_human, :]  # 使用iloc函数将数据块提取出
a.to_excel(
    r'F:/daixie/data/dis_gene_association.xlsx',
    index=False, header=True, engine='xlsxwriter')
  #index,header 是否显示行/列的索引值  engine用于指定要使用的引擎xlsxwriter


#唯一化 circRNA 名字 和 Disease 名字，用来作为关联矩阵的行，列索引。

#Code block 2
# 获取circRNA和disease的唯一索引

#def 自定义函数
def getUniqueIndex(self, data):
# 去重
   circRNAs = data['circRNA Name'].drop_duplicates()
   diseases = data['Disease Name'].drop_duplicates()
   return list(circRNAs), list(diseases)
#list()函数是Python的内置函数。它可以将任何可迭代数据转换为列表类型，并返回转换后的列表。当参数为空时，list函数可以创建一个空列表


#获取每个circRNA所关联的疾病，用列表存储。

#Code block 3
# 获取与单个circRNA所关联的疾病
def search_related_disease(self, circRNA_target):
    diseases_relateWithCircRNA_list = []
    for index_num in range(self.data.shape[0]):
        row_data = self.data.iloc[index_num, :]
        if row_data[0] == circRNA_target:
            diseases_relateWithCircRNA_list.append(row_data[1])
    return diseases_relateWithCircRNA_list


#初步计算circRNA-disease关联矩阵，保存为“ori_association_matrix.xlsx”。

#Code block 4
def construct_ori_association(self) -> pd.DataFrame:
    circRNAs, diseases = self.getUniqueIndex(self.data)
    ori_association_matrix = pd.DataFrame(index=circRNAs, columns=diseases)
    ori_association_matrix.fillna(value=0, inplace=True)
    for circRNA in circRNAs:
        dis_list = self.search_related_disease(circRNA)
        print(dis_list)
        for disease in dis_list:
            ori_association_matrix.loc[circRNA, disease] = 1
    ori_association_matrix.to_excel(
          r'F:\RNA基础\data\ori_association_matrix.xlsx')
    return ori_association_matrix


#对初步产生的circRNA-disease关联矩阵进行数据密集规范化处理。

#设置dropRate，将行或者列关联数小于dropRate的进行删除
#Code block 5



#对列进行密集处理
def drop_columns_of_ori_associationMatrix(self):
     sum_of_cols = self.ori_association_matrix.apply(lambda c: c.sum(), axis=0)
     sum_of_cols = sum_of_cols.sort_values()  # 升序
     # threshold_value = sum_of_cols.iloc[int(sum_of_cols.shape[0] * self.dropColumns_threshold)]    # 用阈值率计算删除数量
     threshold_value = self.dropColumns_threshold
     print('threshold_value_col:', threshold_value)
     for column in self.ori_association_matrix.columns.tolist():
         print(column)
         if sum_of_cols.loc[column] < threshold_value:
             print('sum_of_cols.loc[column]:', sum_of_cols.loc[column])
             self.ori_association_matrix.drop(columns=column, inplace=True)
             print('del_col,Ture')

#Code block 6
# 对行密集处理
def drop_rows_of_ori_associationMatrix(self):
    sum_of_rows = self.ori_association_matrix.apply(lambda r: r.sum(), axis=1)
    sum_of_rows = sum_of_rows.sort_values()
    print(sum_of_rows)
    print('threshold_value_col:', self.dropRows_threshold)
    for row in self.ori_association_matrix.index.tolist():
        print(row)
        if sum_of_rows.loc[row] < self.dropRows_threshold:
            print('sum_of_rows.loc[row]:', sum_of_rows.loc[row])
            self.ori_association_matrix.drop(index=row, inplace=True)
            print('del_row,Ture')

#进行密集处理之后就是我们所需要的关联矩阵
#Code block 7
import pandas as pd


class DataPreprocessing():
    def __init__(self):
        self.data_ori_way = r'F:\RNA基础\data\The circRNA-disease entries of Human.xlsx'
        # self.dropRows_threshold_rate = 0.25
        # self.dropColumns_threshold_rate = 0.25
        self.dropRows_threshold = 1         #去掉稀疏边  这里去掉小于1个1的行
        self.dropColumns_threshold = 1      #去掉稀疏边  这里去掉小于4个1的列

        self.data = self.load_data(self.data_ori_way)
        self.ori_association_matrix = self.construct_ori_association()

    def load_data(self, path) -> pd.DataFrame:
        data_ori = pd.read_excel(path)
        data = data_ori[['circRNA Name', 'Disease Name']]
        return data

    # 获取circRNA和disease的唯一索引
    def getUniqueIndex(self, data):
        circRNAs, diseases = data['circRNA Name'].drop_duplicates(), data['Disease Name'].drop_duplicates()
        return list(circRNAs), list(diseases)

    # 获取与单个circRNA所关联的疾病
    def search_related_disease(self, circRNA_target):
        diseases_relateWithCircRNA_list = []
        for index_num in range(self.data.shape[0]):
            row_data = self.data.iloc[index_num, :]
            if row_data[0] == circRNA_target:
                diseases_relateWithCircRNA_list.append(row_data[1])
        return diseases_relateWithCircRNA_list

    def construct_ori_association(self) -> pd.DataFrame:
        circRNAs, diseases = self.getUniqueIndex(self.data)
        ori_association_matrix = pd.DataFrame(index=circRNAs, columns=diseases)
        ori_association_matrix.fillna(value=0, inplace=True)
        for circRNA in circRNAs:
            dis_list = self.search_related_disease(circRNA)
            print(dis_list)
            for disease in dis_list:
                ori_association_matrix.loc[circRNA, disease] = 1
        ori_association_matrix.to_excel(
            r'F:\RNA基础\data\ori_association_matrix.xlsx')
        return ori_association_matrix

    def drop_columns_of_ori_associationMatrix(self):
        sum_of_cols = self.ori_association_matrix.apply(lambda c: c.sum(), axis=0)
        sum_of_cols = sum_of_cols.sort_values()  # 升序
        # threshold_value = sum_of_cols.iloc[int(sum_of_cols.shape[0] * self.dropColumns_threshold)]    # 用阈值率计算删除数量
        threshold_value = self.dropColumns_threshold
        print('threshold_value_col:', threshold_value)
        for column in self.ori_association_matrix.columns.tolist():
            print(column)
            if sum_of_cols.loc[column] < threshold_value:
                print('sum_of_cols.loc[column]:', sum_of_cols.loc[column])
                self.ori_association_matrix.drop(columns=column, inplace=True)
                print('del_col,Ture')
        # return self.ori_association_matrix

    def drop_rows_of_ori_associationMatrix(self):
        sum_of_rows = self.ori_association_matrix.apply(lambda r: r.sum(), axis=1)
        sum_of_rows = sum_of_rows.sort_values()
        print(sum_of_rows)
        print('threshold_value_col:', self.dropRows_threshold)
        for row in self.ori_association_matrix.index.tolist():
            print(row)
            if sum_of_rows.loc[row] < self.dropRows_threshold:
                print('sum_of_rows.loc[row]:', sum_of_rows.loc[row])
                self.ori_association_matrix.drop(index=row, inplace=True)
                print('del_row,Ture')


if __name__ == '__main__':
    DP = DataPreprocessing()

    # 先删除列
    DP.drop_columns_of_ori_associationMatrix()
    # 后删除行
    DP.drop_rows_of_ori_associationMatrix()

    association_del_col_row = DP.ori_association_matrix

    circRNA_name = association_del_col_row.index.tolist()
    df_c = pd.DataFrame(circRNA_name, columns=['circRNA Name'])
    print(circRNA_name)
    df_c.to_excel(
        r'F:\RNA基础\data\circRNAName.xlsx', index=False)

    disease_name = association_del_col_row.columns.tolist()
    df_d = pd.DataFrame(disease_name, columns=['disease Name'])
    print(disease_name)
    df_d.to_excel(
        r'F:\RNA基础\data\diseaseName.xlsx', index=False)

    association_del_col_row.to_excel(
        r'F:\RNA基础\data\associationMatrix.xlsx',
        index=False, header=False)

    # 关联数统计
    count = 0
    for i in range(association_del_col_row.shape[0]):
        for j in range(association_del_col_row.shape[1]):
            if association_del_col_row.iloc[i, j] == 1:
                count = count + 1

    print(association_del_col_row)
    print('关联数：', count)