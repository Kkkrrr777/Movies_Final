import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

rcParams['font.family'] = 'SimHei'


# 读取CSV文件
df = pd.read_csv('用户信息.csv')

# 统计分析
age_counts = df['age'].value_counts()
sex_counts = df['sex'].value_counts()
address_counts = df['address'].value_counts()
work_counts = df['work'].value_counts()
married_counts = df['married'].value_counts()
type_counts = df['type'].value_counts()

# 绘制不同类型的图像
# fig, axes = plt.subplots(3, 2, figsize=(14, 10))

# 扇形图
plt.figure(figsize=(6, 6))
plt.pie(sex_counts, labels=sex_counts.index, autopct='%1.1f%%')
plt.title('性别')
plt.savefig("./Movies_Recommend-master/static/img/统计图1.png", dpi=300)
plt.close()
# 扇形图
plt.figure(figsize=(6, 6))
plt.pie(work_counts, labels=work_counts.index, autopct='%1.1f%%')
plt.title('工作状态')
plt.savefig("./Movies_Recommend-master/static/img/统计图2.png", dpi=300)
plt.close()
# 条形图
plt.figure(figsize=(8, 6))
plt.bar(age_counts.index, age_counts.values)
plt.title('年龄')
plt.savefig("./Movies_Recommend-master/static/img/统计图3.png", dpi=300)
plt.close()
# 条形图
plt.figure(figsize=(8, 6))
plt.bar(type_counts.index, type_counts.values)
plt.title('工作类型')
plt.savefig("./Movies_Recommend-master/static/img/统计图4.png", dpi=300)
plt.close()
# 扇形图
plt.figure(figsize=(6, 6))
plt.pie(married_counts, labels=married_counts.index, autopct='%1.1f%%')
plt.title('婚姻状态')
plt.savefig("./Movies_Recommend-master/static/img/统计图5.png", dpi=300)
plt.close()
# 条形图
plt.figure(figsize=(8, 6))
plt.bar(address_counts.index, address_counts.values)
plt.title('地区')
plt.xticks(rotation=60, ha='right')  # 设置标签文字倾斜30度，纵向排列
plt.tight_layout()  # 调整布局，防止标签文字被截断
plt.savefig("./Movies_Recommend-master/static/img/统计图6.png", dpi=300)
plt.close()

