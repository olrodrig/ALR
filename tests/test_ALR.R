source('../src/ALR.R')

#input data
x     <- c(0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4)
y     <- c(0.1, 0.2, 0.6, 0.8, 0.9, 0.9, 1.3, 1.4, 1.7, 1.9)
err_y <- 0.1

ALR <- Automated_Loess_Regression(x, y, err_y=err_y)

#evaluate the ALR fit at xi=0.6
xi <- 0.6
print(ALR$interp(xi))

#print some ALR attributes
print(ALR$deg)   #degree of the local polynomials
print(ALR$alpha) #smoothing parameter
print(ALR$enp)   #equivalent number of parameters
