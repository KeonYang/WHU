#%%
import os
import pandas as pd             
import datetime as dt           
from scipy import stats         
import statsmodels.api as sm    
import matplotlib.pyplot as plt 
import seaborn as sns
#%%         
import WindPy as w              
from WindPy import *            
w.start()
#%%
path = os.getcwd()
start = "2008-01-01"
end = "2017-12-31"
#%%
def months_list(start = start, end = end):
    '''
    参数：
        start: 开始日期("YYYY-MM-DD")。(str)
        end: 结束日期("YYYY-MM-DD")。(str)
    返回：
        样本期的月份列表。(string list)
    '''
    file_path = path + r"/months.csv"
    if os.path.isfile(file_path):
        months = pd.read_csv(
            open(file_path, 'r', encoding = 'utf-8'), 
            index_col = [0]
        )[12:]
        months_list = list(months["Month"])
        months_list = [x[:7] for x in months_list] # pandas自动转换了日期，故只取年和月部分
    else:
        months = w.tdays(start, end, "Period=M", usedf = True)[1]
        months.columns = ["Month"]
        months.to_csv(file_path)
        months_list = list(months["Month"])
        months_list = [x.strftime('%Y-%m') for x in months_list] # 日期转字符串
    return months_list
#%%
months_list = months_list()
#%%
def market(
    start = start, 
    end = end, 
    hs300 = False, 
    windA = True, 
):
    '''
    参数：
        start: 开始日期("YYYY-MM-DD")。(str)
        end: 结束日期("YYYY-MM-DD")。(str)
        hs300: 是否用沪深300代表市场指数。(bool)
        windA: 用万德全A代表市场指数。(bool)
    返回：
        市场指数在样本期内的表现。(pd.DataFrame)
        index: Month, 日期(YYYY-MM-DD)。(string)
        column: Market, 当月涨跌幅（%）。(float)
    '''
    file_path = path + r"/market.csv"
    if os.path.isfile(file_path):
        market = pd.read_csv(
            open(file_path, 'r', encoding = 'utf-8'), 
            index_col = [0]
        )[12:]
    else:
        if hs300:
            market_code = "000300.SH"
        elif windA:
            market_code = "881001.WI"
        market = w.wsd(
            market_code, 
            "pct_chg", 
            start, 
            end, 
            "Period=M", 
            usedf = True
        )[1]
        market.index = pd.to_datetime(market.index).strftime("%Y-%m")
        market.index.name = "Month"
        market.columns = ["Market"]
        market.dropna(inplace = True) # 剔除缺失值
        market.to_csv(file_path)
    return market
#%%
market = market()
#%%
def shibor(start = start, end = end):
    '''
    参数：
        start: 开始日期("YYYY-MM-DD")。(str)
        end: 结束日期("YYYY-MM-DD")。(str)
    返回：
        无风险利率，以SHIBOR隔夜利率的月平均值代表。(pd.DataFrame)
        index: Month, 日期(YYYY-MM-DD)。(pd.datetime)
        column: Shibor, 当月涨跌幅（%）。(float)
    '''
    file_path = path + r"/shibor.csv"
    if os.path.isfile(file_path):
        shibor = pd.read_csv(
            open(file_path, 'r', encoding = 'utf-8'), 
            index_col = [0]
        )[12:]
    else:
        shibor = w.wsd(
            "SHIBORON.IR", 
            "close", 
            start, 
            end, 
            "", 
            usedf = True
        )[1]
        shibor.index = pd.to_datetime(shibor.index).strftime('%Y-%m')
        shibor = pd.DataFrame(shibor.groupby(shibor.index)["CLOSE"].mean()) 
        shibor.index.name = "Month"
        shibor.columns = ["Shibor"]
        shibor.dropna(inplace = True) # 剔除缺失值
        shibor.to_csv(file_path)
    return shibor
#%%
shibor = shibor()
#%%
def all_data(
    start = start, 
    end = end, 
    universe = "A", 
    trading_only = True, 
    non_ST_only = True
):
    '''
    参数：
        start: 开始日期("YYYY-MM-DD")。(str)
        end: 结束日期("YYYY-MM-DD")。(str)
        universe: 股票池，沪深300('hs300')或全部A股('A')。(str)
        trading_only: 是否只保留正常交易的股票。(bool)
        non_ST_only: 是否只保留非ST股票。(bool)
    返回：
        指定样本期的全部数据。(pd.DataFrame)
        index: Month, 日期(YYYY-MM)。(str)
        columns:
            Code, 股票代码。(str)
            Name, 股票简称。(str)
            Return, 当月涨跌幅（%）。(float)
            ME, 当月总市值。(float)
            Book, 当月账面价值。(float)
            Price, 当月股价。(float)
            BP, 当月账面市值比。(float)
            Asset, 当月账面价值。(float)
            ROE, 权益回报。(float)
            ST, 是否为ST股票。(str)
    '''
    
    file_path = path + r"/data.csv"

    if os.path.isfile(file_path):
        data = pd.read_csv(
            open(
                file_path, 
                'r', 
                encoding = 'utf-8'
            ), 
            index_col = [0]
        )
        if trading_only:
            data = data.dropna() # 剔除缺失值
        if non_ST_only:
            data = data[data['ST'] == '否'] # 剔除ST股票
        data["Asset"] = data["Asset"].astype("str")
        data["Asset"] = [''.join(x.split(",")) for x in list(data["Asset"])]
        data["Asset"] = data["Asset"].astype("float")

    else:

        if universe == "hs300":
            stocks_list = list(w.wset(
                "sectorconstituent", 
                "date="+end+";windcode=000300.SH", 
                usedf = True
            )[1].sample(100)['wind_code']) # ".sample(100)" 仅测试用
            
        elif universe == "A":
            stocks_list = list(
                w.wset(
                    "sectorconstituent",
                    "date="+end+";sectorid=a001010100000000", 
                    usedf = True
                )[1]['wind_code'] # ".sample(100)" 仅测试用
            )

        data = pd.DataFrame()

        for stock in stocks_list:
            stock_data = w.wsd(
                stock, 
                "trade_code,pct_chg,ev,roe,yoyassets,trade_status,riskwarning", 
                start, 
                end, 
                "unit=1;ruleType=3;period=2;returnType=1;index=000001.SH;Period=M;Fill=Previous", 
                usedf = True
            )[1]
            stock_data.index = pd.to_datetime(stock_data.index).strftime("%Y-%m")
            data = data.append(stock_data)

        data.index.name = "Month"
        data.columns = [
            "Code", "Return", 
            "ME", "ROE", 
            "Asset", "Status", "ST"
        ]

        data.to_csv(file_path)
        
    return data
#%%
data = all_data()
#%%
def excess(data):
    '''
    参数：
        data: 要操作的数据表。(pd.DataFrame)
    返回：
        添加了无风险利率和超额收益列的原数据表。(pd.DataFrame)
    '''
    col_list = list(data.columns)
    data["Shibor"] = list(shibor["Shibor"])
    for column in col_list:
        data[column] = data[column] - data["Shibor"]
    return data[col_list]
#%%
def value_weighted_data(data):
    '''
    参数：
        data: 要操作的数据表。(pd.DataFrame)
    返回：
        将Return列替换为按ME列（市值）加权后的Return。(pd.DataFrame)
    '''
    total_ME = data.sum(axis = 0)["ME"]
    data["Weight"] = data["ME"] / total_ME
    data["Return"] = data["Return"] * data["Weight"]
    return data
#%%
def monthly_return(factor, value_weighted = True):
    '''
    参数：
        factor: 因子指标名。(str)
        value_weighted: 是否将收益市值加权。(bool)
    返回：
        每个月按照因子排列的大小投资组合的收益。(pd.DataFrame)
    '''
    small_ret_list, big_ret_list = [], []
    for month, monthly_data in data.groupby(data.index):
        sort = monthly_data.sort_values(by = factor)
        small = sort[:round(len(monthly_data)/3)]
        big = sort[-round(len(monthly_data)/3):]
        if value_weighted:
            small_ret = value_weighted_data(small).sum(axis = 0)["Return"]
            big_ret = value_weighted_data(big).sum(axis = 0)["Return"]
        else:
            small_ret = small.sum(axis = 0)["Return"]/len(small)
            big_ret = big.sum(axis = 0)["Return"]/len(big)
        small_ret_list.append(small_ret)
        big_ret_list.append(big_ret)
    monthly_return = pd.DataFrame(index = months_list)
    monthly_return["Small " + factor] = small_ret_list
    monthly_return["Big " + factor] = big_ret_list
    return monthly_return
#%%
def MKT(excess_return = True):
    '''
    参数：
        excess_return: 是否计算超额收益。(bool)
    返回：
        指定 Fama French 三因素模型的市场因子。(pd.DataFrame)
    '''
    MKT = market
    MKT.columns = ["MKT"]
    if excess_return:
        MKT = excess(MKT)
    return MKT
#%%
MKT = MKT()
#%%
def SMB(excess_return = True):
    '''
    参数：
        excess_return: 是否计算超额收益。(bool)
    返回：
        指定 Fama French 三因素模型中的HML因子。(pd.DataFrame)
    '''
    data = monthly_return('ME')
    data["SMB"] = data["Small ME"] - data["Big ME"]
    if excess_return:
        data = excess(data)
    return data[["SMB"]]
#%%
SMB = pd.read_csv(path + r"/SMB.csv", index_col = [0])
#%%
SMB.to_csv(path + r"SMB.csv")
#%%
def HML(excess_return = True):
    '''
    参数：
        excess_return: 是否计算超额收益。(bool)
    返回：
        指定 Fama French 三因素模型中的HML因子。(pd.DataFrame)
    '''
    data = monthly_return('BP')
    data["HML"] = data["Big BP"] - data["Small BP"]
    if excess_return:
        data = excess(data)
    return data[["HML"]]
#%%
HML = HML()
#%%
def ROE(excess_return = True):
    '''
    参数：
        excess_return: 是否计算超额收益。(bool)
    返回：
        指定 Fama French 模型中的 ROE 因子。(pd.DataFrame)
    '''
    data = monthly_return("ROE")
    data["ROE"] = data["Big ROE"] - data["Small ROE"] 
    if excess_return:
        data = excess(data)
    return data[["ROE"]]
#%%
ROE = ROE()
#%%
def CMA(excess_return = True):
    '''
    参数：
        excess_return: 是否计算超额收益。(bool)
    返回：
        指定 Fama French 模型中的 CMA 因子。(pd.DataFrame)
    '''
    data = monthly_return("Asset")
    data["CMA"] = data["Big Asset"] - data["Small Asset"] 
    if excess_return:
        data = excess(data)
    return data[["CMA"]]
#%%
CMA = CMA()
#%%
def MOM(excess_return = True):
    '''
    参数：
        excess_return: 是否计算超额收益。(bool)
    返回：
        指定 Fama French 模型中的 MOM 因子。(pd.DataFrame)
    '''
    data = monthly_return("Return")
    data["MOM"] = data["Big Return"] - data["Small Return"] 
    if excess_return:
        data = excess(data)
    return data [["MOM"]]
#%%
MOM = MOM()
#%%
def Y(excess_return = True):
    '''
    参数：
        excess_return: 是否计算超额收益。(bool)
    返回：
        被解释变量。(pd.DataFrame)
    '''
    Y = {}
    for i in range(5):
        for j in range(5):
            Y["ME" + str(i) + "BP" + str(j)] = []
    for month, monthly_data in data.groupby(data.index):
        sort_ME = monthly_data.sort_values(by = "ME")
        sort_BP_ME = monthly_data.sort_values(by = "BP")
        length = round(len(monthly_data)/5)
        for i in range(5):
            for j in range(5):
                ME_list = list(sort_ME[i*length:(i+1)*length]["Code"])
                BP_ME_list = list(sort_BP_ME[j*length:(j+1)*length]["Code"])
                stock_list = [x for x in ME_list if x in BP_ME_list]
                portfolio = monthly_data[monthly_data["Code"].isin(stock_list)]
                portfolio_ret = value_weighted_data(portfolio).sum(axis = 0)["Return"]
                Y["ME" + str(i) + "BP" + str(j)].append(portfolio_ret)
    return pd.DataFrame(Y, index = months_list)
#%%
Y = Y()
#%%
FamaFrench = pd.DataFrame()
FamaFrench["Shibor"] = shibor["Shibor"]
FamaFrench["Market"] = MKT["MKT"]
#FamaFrench["SMB"] = SMB["SMB"]
FamaFrench["HML"] = HML["HML"]
FamaFrench["ROE"] = ROE["ROE"]
FamaFrench["CMA"] = CMA["CMA"]
FamaFrench["MOM"] = MOM["MOM"]
FamaFrench = pd.concat(
    [FamaFrench, Y], 
    axis = 1, 
    sort = False
)
#%%
FamaFrench.to_csv(path + r"/FamaFrench.csv")

#%%
FamaFrench = pd.read_csv(
    open(
        path + r"/FamaFrench.csv", 
        'r', 
        encoding = 'utf-8'
    ), 
    index_col = [0]
)