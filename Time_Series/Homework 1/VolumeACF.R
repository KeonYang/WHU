# load packages
library(lmtest)
library(tseries)
# load data
Data<-read.table("fcst5input.csv", header = TRUE, sep = ',')
volume = Data$NYSEVOL
volume = volume[(48*12+1):(93*12)]
# compute the acf of log volume series
logvol = log(volume)
acf(logvol) # pacf() computes the PACF
# Detrend
Trend = seq(1,length(volume), by =1)
result1 = lm(logvol ~ Trend)
# compute the acf of the detrended series
acf(result1$residuals)
# fit the residual to ARMA(1,1)
res = result1$residuals
result2 = arma(res, order = c(1,1))
summary(result2)

################################
### seasonal dummies ###########
D = matrix(rep(0,80),nrow = 20)
for (i in 1:20)
{
  D[i, 4 - (4-i)%%4] = 1
}
T = seq(1,20,by = 1)
Data = data.frame(time = T, D1 = D[,1], D2 = D[,2], D3 = D[,3], D4 = D[,4])
library(stats)
X = rnorm(20)
Data1 = data.frame(Data,X)
