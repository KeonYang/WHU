# Title: Investment Case II
# Author: Yang Chenyu
# Number: 2016301550186
# Date: 11/13/2018

# First of all, I save the data I need as .csv in the Pycharm environment
# All path is the project itself

# import all the modules that I need
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Question 1--------------------------------------------

TMI = pd.read_csv('STOXX_TMI.csv').sort_index(ascending=False)
TKA = pd.read_csv('TKA.csv').sort_index(ascending=False)
OLE = pd.read_csv('OLE.csv').sort_index(ascending=False)

# Transfer the str into float
TMI['Return'] = TMI['Return'].str.strip('%').astype(float) / 100
TKA['Return'] = TKA['Return'].str.strip('%').astype(float) / 100
OLE['Return'] = OLE['Return'].str.strip('%').astype(float) / 100

# Calculate the risk of these three assets
TMI_risk = TMI['Return'].std()
TKA_risk = TKA['Return'].std()
OLE_risk = OLE['Return'].std()

# Question 3--------------------------------------------

portion1 = np.array([0.35, 0.65])  # risk-free, index
portion2 = np.array([0.3, 0.7])  # risk-free, index
portion3 = np.array([0.3, 0.65, 0.05])  # risk-free, index, TKA
portion4 = np.array([0.3, 0.65, 0.05])  # risk-free, index, OLE

bond = pd.read_csv('German T-Bills.csv').sort_index(ascending=False)
bond['Return'] = bond['Return'].str.strip('%').astype(float) / 100
data = bond

# Merge different DataFrames to get a total data set of returns of 4 assets
for i in ['TMI', 'TKA', 'OLE']:
    data = pd.merge(data, eval(i).iloc[:, [0, 2]], on='Date', how='outer')
data.columns = ['Date', 'Bond', 'TMI', 'TKA', 'OLE']

# Add the returns of different portfolios into the DataFrame
data['portfolio1'] = (data.iloc[:, [1, 2]] * portion1).sum(axis=1)
data['portfolio2'] = (data.iloc[:, [1, 2]] * portion2).sum(axis=1)
data['portfolio3'] = (data.iloc[:, [1, 2, 3]] * portion3).sum(axis=1)
data['portfolio4'] = (data.iloc[:, [1, 2, 4]] * portion4).sum(axis=1)

# save this data for Problem 7
data_dat = data.copy()

# Calculate the risk of the 4 portfolios
port1_risk = data['portfolio1'].std()
port2_risk = data['portfolio2'].std()
port3_risk = data['portfolio3'].std()
port4_risk = data['portfolio4'].std()

# Because the result is different from my prediction, I chose to calculate the correlations
data.iloc[:, 1:5].corr().to_csv('correlation.csv')

# Question 4--------------------------------------------

# The data for this problem is this
data = data.iloc[:, :5]

# Get the excess return
for i in range(2, 5):
    data.iloc[:, i] = data.iloc[:, i] - data.iloc[:, 1]
data = data.iloc[:, [0, 2, 3, 4]]

# Regression for TKA
Y_TKA = data.iloc[:, 2]
X_TKA = data.iloc[:, 1]
X_TKA = sm.add_constant(X_TKA)

# Use statsmodels to do the OLS rather than sklearn
model = sm.OLS(Y_TKA, X_TKA)
results = model.fit()
alpha, beta = results.params
x_fit = np.array(X_TKA)
y_fit = results.fittedvalues

# Calculate the total risk, system risk and nonmarket risk
total_risk_TKA = data.iloc[:, 2].std()
sys_risk_TKA = beta * data.iloc[:, 1].std()
nonsys_risk_TKA = (results.fittedvalues - Y_TKA).std()

# Plot for TKA
plt.scatter(data.iloc[:, 1], data.iloc[:, 2], c='r', label='Actual')
plt.plot(x_fit[:, 1], y_fit, label='OLS', linewidth=2, c='b')
plt.xlabel('TMI')
plt.ylabel('TKA')
plt.title('Single-Index Model for TKA')
plt.xlim(-0.15, 0.15)
plt.ylim(-0.4, 0.3)
plt.grid()
plt.legend()
plt.show()

# Regression for OLE
Y_OLE = data.iloc[:, 3]
X_OLE = data.iloc[:, 1]
X_OLE = sm.add_constant(X_OLE)
model = sm.OLS(Y_OLE, X_OLE)
results = model.fit()
alpha, beta = results.params
x_fit = np.array(X_OLE)
y_fit = results.fittedvalues

# Calculate the total risk, system risk and nonmarket risk
total_risk_OLE = data.iloc[:, 3].std()
sys_risk_OLE = beta * data.iloc[:, 1].std()
nonsys_risk_OLE = (results.fittedvalues - Y_OLE).std()

# Plot for OLE
plt.scatter(data.iloc[:, 1], data.iloc[:, 3], c='r', label='Actual')
plt.plot(x_fit[:, 1], y_fit, label='OLS', linewidth=2, c='b')
plt.xlabel('TMI')
plt.ylabel('OLE')
plt.title('Single-Index Model for OLE')
plt.grid()
plt.xlim(-0.15, 0.15)
plt.ylim(-0.6, 0.6)
plt.legend()
plt.show()

# Question 7--------------------------------------------

# deep copy in order to get original data
data = data_dat.copy()

# Generate Benchmark 40% bonds & 60% market index
benchmark = data.iloc[:, :3]
benchmark['Benchmark'] = (data.iloc[:, [1, 2]] * np.array([0.4, 0.6])).sum(axis=1) - benchmark['Bond']
benchmark['TMI'] = benchmark['TMI'] - benchmark['Bond']
benchmark = benchmark.iloc[:, [0, 2, 3]]

# OLS for benchmark
X_benchmark = benchmark.iloc[:, 1]
X_benchmark = sm.add_constant(X_benchmark)
Y_benchmark = benchmark.iloc[:, 2]
results = sm.OLS(Y_benchmark, X_benchmark).fit()
alpha_bench, beta_bench = results.params

# Calculate the total risk, system risk and nonmarket risk
total_risk_benchmark = benchmark.iloc[:, 2].std()
sys_risk_benchmark = beta_bench * benchmark.iloc[:, 1].std()
nonsys_risk_benchmark = (results.fittedvalues - Y_benchmark).std()

# Generate the excess return of portfolios
data.iloc[:, 2] = data.iloc[:, 2] - data.iloc[:, 1]
for i in range(5, 9):
    data.iloc[:, i] = data.iloc[:, i] - data.iloc[:, 1]
data = data.iloc[:, [0, 2, 5, 6, 7, 8]]

# Portfolio 1
Y_p1 = data.iloc[:, 2]
X_p1 = data.iloc[:, 1]
X_p1 = sm.add_constant(X_p1)
model = sm.OLS(Y_p1, X_p1)
results = model.fit()
alpha_p1, beta_p1 = results.params

# Calculate the total risk, system risk and nonmarket risk
total_risk_p1 = data.iloc[:, 2].std()
sys_risk_p1 = beta_p1 * data.iloc[:, 1].std()
nonsys_risk_p1 = (results.fittedvalues - Y_p1).std()

# Portfolio 2
Y_p2 = data.iloc[:, 3]
X_p2 = data.iloc[:, 1]
X_p2 = sm.add_constant(X_p2)
model = sm.OLS(Y_p2, X_p2)
results = model.fit()
alpha_p2, beta_p2 = results.params

# Calculate the total risk, system risk and nonmarket risk
total_risk_p2 = data.iloc[:, 3].std()
sys_risk_p2 = beta_p2 * data.iloc[:, 1].std()
nonsys_risk_p2 = (results.fittedvalues - Y_p2).std()

# Portfolio 3
Y_p3 = data.iloc[:, 4]
X_p3 = data.iloc[:, 1]
X_p3 = sm.add_constant(X_p3)
model = sm.OLS(Y_p3, X_p3)
results = model.fit()
alpha_p3, beta_p3 = results.params

# Calculate the total risk, system risk and nonmarket risk
total_risk_p3 = data.iloc[:, 4].std()
sys_risk_p3 = beta_p3 * data.iloc[:, 1].std()
nonsys_risk_p3 = (results.fittedvalues - Y_p3).std()

# Portfolio 4
Y_p4 = data.iloc[:, 5]
X_p4 = data.iloc[:, 1]
X_p4 = sm.add_constant(X_p4)
model = sm.OLS(Y_p4, X_p4)
results = model.fit()
alpha_p4, beta_p4 = results.params

# Calculate the total risk, system risk and nonmarket risk
total_risk_p4 = data.iloc[:, 5].std()
sys_risk_p4 = beta_p4 * data.iloc[:, 1].std()
nonsys_risk_p4 = (results.fittedvalues - Y_p4).std()

# Problem 9

data = data_dat.copy()
# Remove the data of 2018
data = data[data['Date'].apply(lambda x: False if x.__contains__('2008') else True)]

# Generate Benchmark 40% bonds & 60% market index
benchmark = data.iloc[:, :3]
benchmark['Benchmark'] = (data.iloc[:, [1, 2]] * np.array([0.4, 0.6])).sum(axis=1) - benchmark['Bond']
benchmark['TMI'] = benchmark['TMI'] - benchmark['Bond']
benchmark = benchmark.iloc[:, [0, 2, 3]]

# OLS for benchmark
X_benchmark = benchmark.iloc[:, 1]
X_benchmark = sm.add_constant(X_benchmark)
Y_benchmark = benchmark.iloc[:, 2]
results = sm.OLS(Y_benchmark, X_benchmark).fit()
alpha_bench, beta_bench = results.params

# Calculate the total risk, system risk and nonmarket risk
total_risk_benchmark = benchmark.iloc[:, 2].std()
sys_risk_benchmark = beta_bench * benchmark.iloc[:, 1].std()
nonsys_risk_benchmark = (results.fittedvalues - Y_benchmark).std()

# Generate the excess return of portfolios
data.iloc[:, 2] = data.iloc[:, 2] - data.iloc[:, 1]
for i in range(5, 9):
    data.iloc[:, i] = data.iloc[:, i] - data.iloc[:, 1]
data = data.iloc[:, [0, 2, 5, 6, 7, 8]]

# Portfolio 1
Y_p1 = data.iloc[:, 2]
X_p1 = data.iloc[:, 1]
X_p1 = sm.add_constant(X_p1)
model = sm.OLS(Y_p1, X_p1)
results = model.fit()
alpha_p1, beta_p1 = results.params

# Calculate the total risk, system risk and nonmarket risk
total_risk_p1 = data.iloc[:, 2].std()
sys_risk_p1 = beta_p1 * data.iloc[:, 1].std()
nonsys_risk_p1 = (results.fittedvalues - Y_p1).std()

# Portfolio 2
Y_p2 = data.iloc[:, 3]
X_p2 = data.iloc[:, 1]
X_p2 = sm.add_constant(X_p2)
model = sm.OLS(Y_p2, X_p2)
results = model.fit()
alpha_p2, beta_p2 = results.params

# Calculate the total risk, system risk and nonmarket risk
total_risk_p2 = data.iloc[:, 3].std()
sys_risk_p2 = beta_p2 * data.iloc[:, 1].std()
nonsys_risk_p2 = (results.fittedvalues - Y_p2).std()

# Portfolio 3
Y_p3 = data.iloc[:, 4]
X_p3 = data.iloc[:, 1]
X_p3 = sm.add_constant(X_p3)
model = sm.OLS(Y_p3, X_p3)
results = model.fit()
alpha_p3, beta_p3 = results.params

# Calculate the total risk, system risk and nonmarket risk
total_risk_p3 = data.iloc[:, 4].std()
sys_risk_p3 = beta_p3 * data.iloc[:, 1].std()
nonsys_risk_p3 = (results.fittedvalues - Y_p3).std()

# Portfolio 4
Y_p4 = data.iloc[:, 5]
X_p4 = data.iloc[:, 1]
X_p4 = sm.add_constant(X_p4)
model = sm.OLS(Y_p4, X_p4)
results = model.fit()
alpha_p4, beta_p4 = results.params

# Calculate the total risk, system risk and nonmarket risk
total_risk_p4 = data.iloc[:, 5].std()
sys_risk_p4 = beta_p4 * data.iloc[:, 1].std()
nonsys_risk_p4 = (results.fittedvalues - Y_p4).std()
