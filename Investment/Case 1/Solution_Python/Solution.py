# 投资学案例分析作业
# 作者：杨宸宇
# 学号：2016301550186

# 调用所需的包
import os
import pandas as pd
import numpy as np
from sympy import Symbol
from sympy.solvers import solve
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# 第一题-----------------------------------------------

# 导入准备好的excel数据, 单独赋值
os.chdir(path=r'/Users/mac/Desktop')
data = pd.read_excel('Investment.xlsx')
data.set_index(keys=data.iloc[:, 0], inplace=True)

# 转换为array方便后面运算
expected_return = np.array(data.iloc[0:3, 1])
standard_variance = np.array(data.iloc[0:3, 2])
correlation = np.array(data.iloc[0:3, 3:6])
# 计算协方差矩阵
corvariance = standard_variance * correlation * standard_variance \
    .reshape(3, 1)
# 由题目知
weight = np.array([0.55, 0.3, 0.15])
STP_expected_return = 0.032

# 计算LTP的预期收益率和波动性
LTP_expected_return = np.sum(weight * expected_return)
LTP_expected_volatility = np.sqrt(np.dot(weight.T, \
                                         np.dot(corvariance, weight)))


# 最优组合配比
def opt(bias):
    return (LTP_expected_return - STP_expected_return) \
           / (bias * np.square(LTP_expected_volatility))


# bias = 16
y1 = opt(16)

# bias = 8
y2 = opt(8)

# 画无差异曲线取 u = 0.05 和 u = 0.09, A = 4(bias) 和 A = 8(bias)

# A = 4, u = 0.05
A = 4
u = 0.05
standard_variances = np.linspace(0, 0.5, 100)
expected_returns = []
for std in standard_variances:
    x = Symbol('x')
    expected_return = solve(x - 0.5 * A * np.square(std) - u, x)[0]
    expected_returns.append(expected_return)
standard_variances = np.array(standard_variances)
expected_returns = np.array(expected_returns)

plt.plot(standard_variances, expected_returns, \
         label='A = 4, u = 0.05', c='blue')

# A = 4, u = 0.09
A = 4
u = 0.09
standard_variances = np.linspace(0, 0.5, 100)
expected_returns = []
for std in standard_variances:
    x = Symbol('x')
    expected_return = solve(x - 0.5 * A * np.square(std) - u, x)[0]
    expected_returns.append(expected_return)
standard_variances = np.array(standard_variances)
expected_returns = np.array(expected_returns)

plt.plot(standard_variances, expected_returns, \
         label='A = 4, u = 0.09', c='blue', linestyle='--')

# A = 8, u = 0.05
A = 8
u = 0.05
standard_variances = np.linspace(0, 0.5, 100)
expected_returns = []
for std in standard_variances:
    x = Symbol('x')
    expected_return = solve(x - 0.5 * A * np.square(std) - u, x)[0]
    expected_returns.append(expected_return)
standard_variances = np.array(standard_variances)
expected_returns = np.array(expected_returns)

plt.plot(standard_variances, expected_returns, \
         label='A = 8, u = 0.05', c='red')

# A = 8, u = 0.09
A = 8
u = 0.09
standard_variances = np.linspace(0, 0.5, 100)
expected_returns = []
for std in standard_variances:
    x = Symbol('x')
    expected_return = solve(x - 0.5 * A * np.square(std) - u, x)[0]
    expected_returns.append(expected_return)
standard_variances = np.array(standard_variances)
expected_returns = np.array(expected_returns)

plt.plot(standard_variances, expected_returns, \
         label='A = 8, u = 0.09', c='red', linestyle='--')

# CAL
k = (LTP_expected_return - STP_expected_return) / LTP_expected_volatility
b = 0.032
y = 0.5 * k + b
plt.plot([0, 0.5], [0.032, y], label='CAL', linewidth=2, c='black')
plt.axis([0, 0.5, 0, 1.1])
plt.grid(True)
plt.xlabel('Expected Volatility')
plt.ylabel('Expected Return')
plt.title('Indifference Curve')
plt.legend()
plt.show()

# 第二题-----------------------------------------------

# 导入准备好的excel数据, 单独赋值
os.chdir(path=r'/Users/mac/Desktop')
data = pd.read_excel('Investment.xlsx')
data.set_index(keys=data.iloc[:, 0], inplace=True)

# 转换为array方便后面运算
expect_return = np.array(data.iloc[0:3, 1])
standard_variance = np.array(data.iloc[0:3, 2])
correlation = np.array(data.iloc[0:3, 3:6])

# 计算协方差矩阵
corvariance = standard_variance * correlation * standard_variance \
    .reshape(3, 1)

# 采用蒙特卡洛方法来来绘制资产组合的分布图
expect_returns = []
risks = []
for i in range(10000):
    weights = np.random.random(3)
    # 随机生成资产权重
    weights /= np.sum(weights)
    por_return = np.sum(weights * expect_return)
    por_risk = np.sqrt(np.dot(weights.T, np.dot(corvariance, weights)))
    expect_returns.append(por_return)
    risks.append(por_risk)
# matplotlib.pyplot倾向于np.array格式，因此进行转换
expect_returns = np.array(expect_returns)
risks = np.array(risks)
# 无风险利率定为3.2%(文章中2005年STP的收益率)
risk_free_rate = 0.032

plt.scatter(risks, expect_returns, \
            c=(expect_returns - risk_free_rate) / risks, marker='o', s=8)
plt.grid(True)
plt.xlabel('Risk')
plt.ylabel('Expected Return')
plt.title('Portfolios')
plt.colorbar(label='Sharpe ratio')

# 找出Sharpe最大的点，利用Scipy.optimize.minimize进行凸优化

max_Sharpe = lambda x: - ((np.sum(x * expect_return) - risk_free_rate) / \
                          np.sqrt(np.dot(x.T, np.dot(corvariance, x))))
cons = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
bnds = tuple((0, 1) for x in range(3))
x0 = np.array([1 / 3, 1 / 3, 1 / 3])
# 将优化结果储存到result中
result = minimize(max_Sharpe, x0, method='SLSQP', bounds=bnds, \
                  constraints=cons)
weight = result['x']
expected_return = np.sum(weight * expect_return)
risk = np.sqrt(np.dot(weight.T, np.dot(corvariance, weight)))
# A点为Sharpe值最大的资产组合在图中的坐标
A = (risk, expected_return)
# 画出Sharpe最大的点
plt.plot(risk, expected_return, 'r*', markersize=15.0)
# 为了美观确定坐标轴的刻度范围
plt.axis([0, 0.17, 0, 0.15])

# 找出Risk最低的点

min_risk = lambda x: np.sqrt(np.dot(x.T, np.dot(corvariance, x)))
cons = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
bnds = tuple((0, 1) for x in range(3))
x0 = np.array([1 / 3, 1 / 3, 1 / 3])
result = minimize(min_risk, x0, method='SLSQP', bounds=bnds, \
                  constraints=cons)
weight = result['x']
expected_return = np.sum(weight * expect_return)
risk = np.sqrt(np.dot(weight.T, np.dot(corvariance, weight)))
# 画出Risk最低的点
plt.plot(risk, expected_return, 'y*', markersize=15.0)

# 寻找并画出有效边界
expected_returns = np.linspace(0.055, 0.128, 100)
risks = []
for i in expected_returns:
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1}, \
            {'type': 'eq', 'fun': lambda x: np.sum(x * expect_return) - i})
    result = minimize(min_risk, x0, method='SLSQP', \
                      constraints=cons, bounds=bnds)
    risks.append(result['fun'])
plt.scatter(risks, expected_returns, c='red', marker='x', s=14)
asserts3_risks = np.array(risks)
asserts3_return = np.array(expected_returns)
# 画出资产配置线，理论上应该凸优化求出最大k，但因为之前求了Sharpe最大组合，因此选择直接画
k = (A[1] - 0.032) / A[0]
b = 0.032
x = 0.14
y = k * x + b
plt.plot([0, 0.14], [0.032, y], c='blue')

# 显示图像
plt.show()

# 第三题-----------------------------------------------

# 导入准备好的excel数据,单独赋值,文件位置在本机的desktop处
os.chdir(path=r'/Users/mac/Desktop')
data = pd.read_excel('Investment.xlsx')
data.set_index(keys=data.iloc[:, 0], inplace=True)

# 转换为array方便后面运算
expect_return = np.array(data.iloc[:, 1])
standard_variance = np.array(data.iloc[:, 2])
correlation = np.array(data.iloc[:, 3:])
US_risk = standard_variance[0]
US_return = expect_return[0]
Foreign_risk = standard_variance[1]
Foreign_return = expect_return[1]
Bonds_risk = standard_variance[2]
Bonds_return = expect_return[2]
REITs_risk = standard_variance[3]
REITs_return = expect_return[3]
Commodities_risk = standard_variance[4]
Commodities_return = expect_return[4]

# 计算协方差矩阵
corvariance = standard_variance * correlation * standard_variance \
    .reshape(5, 1)

# 采用蒙特卡洛方法来来绘制资产组合的分布图
expect_returns = []
risks = []
for i in range(10000):
    weights = np.random.random(5)
    weights /= np.sum(weights)
    por_return = np.sum(weights * expect_return)
    por_risk = np.sqrt(np.dot(weights.T, np.dot(corvariance, weights)))
    expect_returns.append(por_return)
    risks.append(por_risk)
expect_returns = np.array(expect_returns)
risks = np.array(risks)
# 无风险利率定为3.2%(文章中2005年STP的收益率)
risk_free_rate = 0.032

plt.scatter(risks, expect_returns, \
            c=(expect_returns - risk_free_rate) / risks, marker='o', s=8)
plt.grid(True)
plt.xlabel('Risk')
plt.ylabel('Expected Return')
plt.title('Portfolios')
plt.colorbar(label='Sharpe ratio')

# 找出Sharpe最大的点

max_Sharpe = lambda x: - ((np.sum(x * expect_return) - risk_free_rate) / \
                          np.sqrt(np.dot(x.T, np.dot(corvariance, x))))
cons = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
bnds = tuple((0, 1) for x in range(5))
x0 = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
result = minimize(max_Sharpe, x0, method='SLSQP', bounds=bnds, \
                  constraints=cons)
weight = result['x']
expected_return = np.sum(weight * expect_return)
risk = np.sqrt(np.dot(weight.T, np.dot(corvariance, weight)))
A = (risk, expected_return)
# 画出Sharpe最大的点
plt.plot(risk, expected_return, 'r*', markersize=15.0)
plt.axis([0, 0.17, 0, 0.13])

# 找出Risk最低的点

min_risk = lambda x: np.sqrt(np.dot(x.T, np.dot(corvariance, x)))
cons = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
bnds = tuple((0, 1) for x in range(5))
x0 = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
result = minimize(min_risk, x0, method='SLSQP', bounds=bnds, \
                  constraints=cons)
weight = result['x']
expected_return = np.sum(weight * expect_return)
risk = np.sqrt(np.dot(weight.T, np.dot(corvariance, weight)))
# 画出Risk最低的点
plt.plot(risk, expected_return, 'y*', markersize=15.0)

# 找出并画出有效边界
expected_returns = np.linspace(0.055, 0.124, 100)
risks = []
for i in expected_returns:
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1}, \
            {'type': 'eq', 'fun': lambda x: np.sum(x * expect_return) - i})
    result = minimize(min_risk, x0, method='SLSQP', \
                      constraints=cons, bounds=bnds)
    risks.append(result['fun'])
plt.scatter(risks, expected_returns, c='red', marker='x', s=14)
asserts5_risks = risks
asserts5_return = expected_returns
plt.plot()

# 画出资产配置线
k = (A[1] - 0.032) / A[0]
b = 0.032
x = 0.12
y = k * x + b
plt.plot([0, 0.12], [0.032, y], c='blue')

# 显示图像
plt.show()

# 和REITs的4种资产组合
expect_return = np.array(data.iloc[:4, 1])
standard_variance = np.array(data.iloc[:4, 2])
correlation = np.array(data.iloc[:4, 3:7])

# 计算协方差矩阵
corvariance = standard_variance * correlation * standard_variance \
    .reshape(4, 1)

# 找出并画出有效边界
expected_returns = np.linspace(0.055, 0.124, 100)
risks = []
x0 = np.array([0.25, 0.25, 0.25, 0.25])
bnds = tuple((0, 1) for x in range(4))
for i in expected_returns:
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1}, \
            {'type': 'eq', 'fun': lambda x: np.sum(x * expect_return) - i})
    result = minimize(min_risk, x0, method='SLSQP', \
                      constraints=cons, bounds=bnds)
    risks.append(result['fun'])
asserts4_REITs_risks = risks
asserts4_REITs_return = expected_returns

# 和Commodities的4种资产组合
expect_return = np.array(data.iloc[[0, 1, 2, 4], 1])
standard_variance = np.array(data.iloc[[0, 1, 2, 4], 2])
correlation = np.array(data.iloc[[0, 1, 2, 4], [3, 4, 5, 7]])

# 计算协方差矩阵
corvariance = standard_variance * correlation * standard_variance \
    .reshape(4, 1)

# 找出并画出有效边界
expected_returns = np.linspace(0.055, 0.124, 100)
risks = []
for i in expected_returns:
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1}, \
            {'type': 'eq', 'fun': lambda x: np.sum(x * expect_return) - i})
    result = minimize(min_risk, x0, method='SLSQP', \
                      constraints=cons, bounds=bnds)
    risks.append(result['fun'])
asserts4_Commodities_risks = risks
asserts4_Commodities_return = expected_returns

plt.plot(asserts3_risks, asserts3_return, c='red', label='3Asserts')
plt.plot(asserts4_REITs_risks, asserts4_REITs_return, c='yellow', label='+REITs')
plt.plot(asserts4_Commodities_risks, asserts4_Commodities_return, c='blue', label='+Commodities')
plt.plot(asserts5_risks, asserts5_return, c='green', label='5Asserts')
plt.scatter(US_risk, US_return, c='red', label='US Equity')
plt.scatter(Foreign_risk, Foreign_return, c='blue', label='Foreign Equity')
plt.scatter(Bonds_risk, Bonds_return, c='green', label='Bonds')
plt.scatter(REITs_risk, REITs_return, c='brown', label='REITs')
plt.scatter(Commodities_risk, Commodities_return, c='orange', label='Commodities')
plt.legend()
plt.grid(True)
plt.xlabel('Risk')
plt.ylabel('Expected Return')
plt.title('Different Asserts')
plt.show()
