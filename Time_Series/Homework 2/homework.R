# Topic: The Homework in Analysis of Time Series

# Name: YANG CHENYU
# Class: Financial Engineering 2
# Student ID:2016301550186

# load package----------------------------------------------
library(tseries)
library(lmtest)
library(tidyverse)
library(zoo)
library(forecast)

# set workspace----------------------------------------------
setwd('/Users/mac/Desktop/R_Time_Analysis/Homework 2')


# input data----------------------------------------------
data = read_csv('VIX1.csv')

# 1-------------------------------------------------------
sample_data <- filter(data, Date < as.Date('2005-1-1'))
sample_vix <- ts(sample_data$VIX, frequency = 52)
detrend_result <- stl(sample_vix, s.window = 'periodic')
detrend <- zoo(detrend_result$time.series, order.by = sample_data$Date)
clean_data <- detrend_result$time.series[,"remainder"]
plot(detrend)

# 2-------------------------------------------------------
plot(arma(clean_data,order = c(1,0))$fitted.values,main = 'AR(1)')
plot(arma(clean_data,order = c(0,1))$fitted.values,main = 'MA(1)')
plot(arma(clean_data,order = c(1,1))$fitted.values,main = 'ARMA(1,1)')


ar.model <- arima(clean_data,order = c(1,0,0))
ma.model <- arima(clean_data,order = c(0,0,1))
arma.model <- arima(clean_data, order =c(1,0,1))

# resulets I needed
ar.model$aic
ma.model$aic
arma.model$aic

actual <- zoo(clean_data,order.by = sample_data$Date)
fitted <- zoo(arma(clean_data,order = c(1,1))$fitted.values,order.by = sample_data$Date)
residual <- zoo(arma(clean_data,order = c(1,1))$residuals,order.by = sample_data$Date)

plot(actual, type = "l", ylim = c(-5, 5),main='AR.model',
     ylab = "Actual(Fitted)",xlab = "time", lty = 2)

par(new = TRUE)
plot(fitted, type = "l", ylim = c(-5, 5),
     ylab = "", xlab = "",lty = 3)

par(new = TRUE)
plot(residual,type="l",ylim = c(-2.5, 15),ylab = "", xlab = "",lty = 1, axes =FALSE)
axis(side = 4, at = c(seq(-2.5, 10.5, by = 1)), lab = c(seq(-2.5, 10.5,by = 1)), 
     ylab = "Residual", xlab = "")

legend("topleft", c("Actual","Residual", "Fitted" ), cex = 0.8,lty = c(2,1,3))



# 3-------------------------------------------------------
summary(ar.model)
forecast_data <- forecast(ar.model, h=47)
plot(forecast_data)
