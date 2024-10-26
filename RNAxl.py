import requests


def fetch_rna_sequence(rna_name):
    # 构造查询的URL
    query_url = f"https://www.cricbase.org/sequence/{rna_name}"

    # 发起HTTP GET请求获取序列页面内容
    response = requests.get(query_url)

    # 检查响应状态码
    if response.status_code == 200:
        # 提取RNA序列
        rna_sequence = response.text

        # 返回RNA序列
        return rna_sequence
    else:
        # 请求失败，返回空序列
        return None


# 从本地读取RNA序列名列表
rna_names = []
with open("F:\RNA基础\data\circRNAName.xlsx", "r", encoding="utf-8") as file:
    for line in file:
        rna_names.append(line.strip())

# 遍历RNA序列名列表，逐个爬取RNA序列
for rna_name in rna_names:
    # 爬取RNA序列
    rna_sequence = fetch_rna_sequence(rna_name)

    # 打印RNA序列结果
    if rna_sequence:
        print(f"RNA Name: {rna_name}")
        print(f"RNA Sequence: {rna_sequence}")
        print("-----------------------")
    else:
        print(f"Failed to fetch RNA sequence for: {rna_name}")