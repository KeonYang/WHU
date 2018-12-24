#%%
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
plt.rcParams.update({"font.size": 11})
import numpy as np
import statsmodels.api as sm
from IPython.display import display
import seaborn as sns
#%%
path = os.getcwd()

#%%
data = pd.read_csv(
    open(
        path + "\\FamaFrench.csv", 
        'r', 
        encoding = "utf-8"
    ), 
    index_col = [0]
)
data.index = pd.to_datetime(data.index, format = '%b-%y').strftime('%Y-%m')

#%% [markdown]
# # 收益率
# 可以看到，动量因子的收益率远高于其它因子，尤其是在2015年中。其余因子的收益率表现相差不大，均值都低于0。

#%%
plt.figure(figsize = (12, 8))
ax = plt.axes()
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
plt.xticks(rotation = 70)
plt.plot(data.index, data["Shibor"], label = "Shibor")
plt.plot(data.index, data["Market"], label = "Market")
plt.plot(data.index, data["SMB"], label = "SMB")
plt.plot(data.index, data["HML"], label = "HML")
plt.plot(data.index, data["ROE"], label = "ROE")
plt.plot(data.index, data["CMA"], label = "CMA")
plt.plot(data.index, data["CMA"], label = "CMA")
plt.plot(data.index, data["MOM"], label = "MOM")
plt.legend()
plt.ylabel("Return(%)")
plt.title("Return of Factors")

#%%
data.describe()

#%% [markdown]
# # 统计报告

#%% [markdown]
# ## 因子间相关性
# 因子间的相关性比较大，这使得模型可能出现过拟合。其中HML和SMB、ROE和SMB等因子间的相关性特别高。如图为SMB和HML的图例。

#%%
factors = list(data.columns[1:7])
correlation = pd.DataFrame(index = factors, columns = factors)
for factor_x in factors:
    for factor_y in factors:
        correlation.loc[factor_x, factor_y] = np.corrcoef(
            data[factor_x], data[factor_y]
        )[0][1]
correlation

#%%
sns.lmplot("HML", "SMB", data)

#%% [markdown]
# ## 因子参数
# 在25个分组的被解释变量中，因子的系数值相差不大，模型对不同风格的投资组合的解释性比较强。
# 
# 其中系数相对较大的有 $\beta$ 和SMB。

#%%
for factor in factors:
    parameters = pd.DataFrame(
        index = ["ME" + str(i) for i in range(5)], 
        columns = ["BP" + str(i) for i in range(5)]
    )
    parameters.index.name = "Parameters of " + factor
    for i in range(5):
        for j in range(5):
            y = list(data["ME" + str(i) + "BP" + str(j)])
            x = data.loc[:, ["Market", "SMB", "HML", "ROE", "CMA", "MOM"]]
            x = sm.add_constant(x)
            result = sm.OLS(y, x).fit()
            parameters.iloc[i, j] = result.params[factor]
    display(parameters)

#%% [markdown]
# ## 因子 t 值
# 
# 因子的 t 值指出其统计显著性。大部分的因子都至少在部分投资组合上展现出显著性。尤其是 Market 和 SMB 因子。

#%%
for factor in factors:
    tvalues = pd.DataFrame(
        index = ["ME" + str(i) for i in range(5)], 
        columns = ["BP" + str(i) for i in range(5)]
    )
    tvalues.index.name = "t values of " + factor
    for i in range(5):
        for j in range(5):
            y = list(data["ME" + str(i) + "BP" + str(j)])
            x = data.loc[:, ["Market", "SMB", "HML", "ROE", "CMA", "MOM"]]
            x = sm.add_constant(x)
            result = sm.OLS(y, x).fit()
            tvalues.iloc[i, j] = result.tvalues[factor]
    display(tvalues)

#%% [markdown]
# ## 因子的$R^2$
# 
# $R^2$ 统计模型对数据的解释性，可以看到模型的解释性良好，在不同被解释变量中的平均值高达89.61%。最好的有92.82%，最差的也有41.72%。

#%%
rsquared = pd.DataFrame(
    index = ["ME" + str(i) for i in range(5)], 
    columns = ["BP" + str(i) for i in range(5)]
)
rsquared.index.name = "R square of Regression"
for i in range(5):
    for j in range(5):
        y = list(data["ME" + str(i) + "BP" + str(j)])
        x = data.loc[:, ["Market", "SMB", "HML", "ROE", "CMA", "MOM"]]
        x = sm.add_constant(x)
        result = sm.OLS(y, x).fit()
        rsquared.iloc[i, j] = result.rsquared
display(rsquared)

#%% [markdown]
# ## 因子修正后的$R^2$
# 修正后的$R^2$有相似的表现。平均值达到89.06%。

#%%
rsquared_adj = pd.DataFrame(
    index = ["ME" + str(i) for i in range(5)], 
    columns = ["BP" + str(i) for i in range(5)]
)
rsquared_adj.index.name = "Adjusted R square of Regression"
for i in range(5):
    for j in range(5):
        y = list(data["ME" + str(i) + "BP" + str(j)])
        x = data.loc[:, ["Market", "SMB", "HML", "ROE", "CMA", "MOM"]]
        x = sm.add_constant(x)
        result = sm.OLS(y, x).fit()
        rsquared_adj.iloc[i, j] = result.rsquared_adj
display(rsquared_adj)

#%% [markdown]
# ## 回归报告
# 取其中一个被解释变量展示回归结果。

#%%
y = list(data["ME4BP0"])
x = data.loc[:, ["Market", "SMB", "HML", "ROE", "CMA", "MOM"]]
x = sm.add_constant(x)
result = sm.OLS(y, x).fit()
print(result.summary())

#%% [markdown]
# ## 因子回归图

#%%
fig = plt.figure(figsize = (12, 8))
fig = sm.graphics.plot_partregress_grid(result, fig = fig)