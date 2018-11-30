#setwd("H:/course/elements of forcasting/code/code element forcasting/DataAndCode/ElementsOfForecasting/fcst_02")
#rm(list=ls())

# Packages------------------------------------------
#library(plotrix)
library(zoo)
library(lmtest)
library(quadprog)
library(tseries)
library(graphics)
# To detect which line the data start from, here the first line is the variable name
#readLines("fcst2input.dat", n=10)
#data2<-read.delim("fcst2input.dat", header = TRUE)
#typeof(data1)
#data1<-read.table("fcst2input.dat", header = TRUE)


# Load data----------------------------------------------
Data1<-read.csv("fcst2input.csv",header = T, sep = ',')
typeof(Data1)
row=nrow(Data1)

# OLS estimation of Y on X and Z with intercept------------------------------------------------
result=lm(Y~X+Z, data=Data1)
# result = lm(Data1$Y ~ Data1$X + Data1$Z)
summary(result)
sum(result$residuals^2)                                   # Sum squared resid
MSE = sum(result$residuals^2)/nrow(data1)                 # MSE of regression
SE_2  = sum(result$residuals^2)/(nrow(data1)-ncol(data1)) # Variance of regression
SE    = sqrt(SE_2)                                        # Standard error of regression
logLik(result)                                            # loglikelihood and degrees of freedom
AIC(result)                                               # AIC of the model
AIC(result, k=log(nrow(data1)))                           # BIC(SIC) of the model
dwtest(result, alternative = "greater")                   # DW test with different alterbatives, "greater" means greater than 0
#dwtest(result, alternative = "two.sided")                # The alternative is that the correlation coefficient is not equal to 0
#dwtest(result, alternative = "less")                     # The alternative is that the correlation coefficient is less than 0
jarque.bera.test(result$residuals)                        # JB test


# Figue 2.4 in the textbook------------------------------------------------------------
# Plot data----------------------
Y = Data1$Y
plot(Y,type="l",axes=FALSE,ylim=c(-4,14),xlab="",ylab="",main="",col="red")
#axis(side=4,at=c(seq(-2,14,by=2)),lab=c(seq(-2,14,by=2)),cex.axis=0.8)

box()
# Plot fitted value---------------
par(new=TRUE) # reset all arguments
plot(result$fitted.values,type="l",axes=FALSE,ylim=c(-4,14),xlab="",ylab="",main="",col="green")
axis(side=4,at=c(seq(0,14,by=2)),lab=c(seq(0,14,by=2)),cex.axis=0.8)

# Plot residual value---------------
par(new=TRUE)
plot(result$residuals,type="l",axes=FALSE,ylim=c(-4,8),xlab="",ylab="",main="",col="blue")
axis(side=2,at=c(seq(-4,8,by=2)),lab=c(seq(-4,8,by=2)),cex.axis=0.8)
abline(h=0,col="black")
abline(h=-2,col="black",lty="dashed")
abline(h=2,col="black",lty="dashed")

# Plot the x axis-------------------------
axis(side=1,at=c(seq(-4,row+3,by=5)),lab=c(seq(1955,2010,by=5)),cex.axis=1)
legend(row-8,-1,c("Residual","Actual","Fitted"),lty=c(1,1),col=c("blue","red","green"),cex=0.5)


#twoord.plot(1:row,result$residuals,1:row,
#            result$fitted.values,
#            #cbind(Y, result$fitted.values),
#            xlab="Sequence",
#            #lylim=range(going_up)+c(-1,10),
#            lylim=c(-4,8),
#            #rylim=range(going_down)+c(-10,2),
#            rylim=c(-2,14),
#            ylab="True&Fitted values",ylab.at=2,
#            rylab="Residuals", rylab.at=7,
#            lcol=4,main="fitted and residuals - separated lines",
#            lytickpos=seq(-4,8,by=2),rytickpos=seq(2,14,by=2)
#            #do.first="plot_bg();grid(col=\"white\",lty=1)"
#            )
#legend(row-8,-1,c("Residual","Actual","Fitted"),lty=c(1,1),col=c("blue","red","green"),cex=0.5)
#abline(h=0,col="black")
#abline(h=-2,col="black",lty="dashed")
#abline(h=2,col="black",lty="dashed")
#lines(Y,type="l",col="red")


