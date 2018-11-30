# construct the data
asset.names = c('US Equity',	'Foreign Equity',	'Bonds',	'REITs',	'Commodities')
er = c(12.94/100,12.42/100, 5.40/100,9.44/100,10.05/100)
names(er) = asset.names

covmat = matrix(c( 0.02313441,  0.01361721,  0.00422078,  0.01153283, -0.00056064,
 0.01361721,  0.02085136,  0.0009617 ,  0.0078207 ,  0.00026613,
 0.00422078,  0.0009617 ,  0.012321  ,  0.0024047 , -0.00143201,
 0.01153283,  0.0078207 ,  0.0024047 ,  0.01833316, -0.00024954,
-0.00056064,  0.00026613, -0.00143201, -0.00024954,  0.03396649), nrow = 5, ncol = 5)
r.free = 0.032
dimnames(covmat) = list(asset.names, asset.names)

# tangency portfolio
tan.port <- tangency.portfolio(er, covmat, r.free)
# compute global minimum variance portfolio
gmin.port = globalMin.portfolio(er, covmat)

# compute portfolio frontier
ef <- efficient.frontier(er, covmat, alpha.min=-2,
                         alpha.max=1.5, nport=20)
attributes(ef)

plot(ef)
plot(ef, plot.assets=TRUE, col="blue", pch=16)
points(gmin.port$sd, gmin.port$er, col="green", pch=16, cex=2)
points(tan.port$sd, tan.port$er, col="red", pch=16, cex=2)
text(gmin.port$sd, gmin.port$er, labels="GLOBAL MIN", pos=2)
text(tan.port$sd, tan.port$er, labels="TANGENCY", pos=2)
sr.tan = (tan.port$er - r.free)/tan.port$sd
abline(a=r.free, b=sr.tan, col="green", lwd=2)