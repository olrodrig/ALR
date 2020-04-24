# Automated loess regression

In regression problems, a parametric model for the response (or dependent) variable as a function of the predictor (or independent) ones is not always available or known. In those cases, a non-parametric regression is highly recommended because it avoids the assumption of a heuristic model. However, the price to pay is that more data are needed to perform a fit, compared to the case of parametric regressions.

One of those non-parametric regressions is **loess** (Cleveland et al. 1992, chapter 8 of [Statistical Models in S](https://ui.adsabs.harvard.edu/abs/1992sms..book.....C/abstract)), which performs polynomial fits over local intervals along the domain. To perform a loess regression with one predictor, it is necessary to specify the order of the local polynomial (deg), which can be 1 (linear) or 2 (quadratic), and the smoothing parameter (alpha), which determines how much of the data is used to fit each local polynomial.

In [Rodríguez et al. (2019)](https://ui.adsabs.harvard.edu/abs/2019MNRAS.483.5459R/abstract), I developed an automated routine to perform **loess** regressions to data with one predictor variable, called **Automated Loess Regression (ALR)**. This routine takes into account the observed and intrinsic errors, along with the presence of possible outliers. The routine uses by default an order 2 for the local polynomials in order to give more freedom to the **loess** fitting procedure. In order to estimate an optimal alpha value, **ALR** uses the "an" information criterion (AIC, [Akaike 1974](https://doi.org/10.1109/TAC.1974.1100705)). To test whether response errors can account for the observed dispersion around the **ALR** fit, the code computes its log-likelihood. If an intrinsic error is necessary to maximize the log-likelihood, then it is added in quadrature to the response errors and the code performs again the **ALR** fit. This process is repeated until an intrinsic error is not necessary. For the outliers detection, **ALR** uses the [Tukey (1977)](https://www.pearson.com/us/higher-education/product/Tukey-Exploratory-Data-Analysis/9780201076165.html) rule, where values below Q1-1.5(Q3-Q1) or above Q3+1.5(Q3-Q1) (known as inner fences, where Q1 and Q3 are the first and third quartile, respectively) are considered as outliers. Finally, the code computes the errors around the **ALR** fit through simulations.

When **loess** is not able to perform a regression (e.g., only few data points are available), then the **ALR** just performs a linear interpolation between points. 

I developed the **ALR** with the purpose of fitting [light curves](https://en.wikipedia.org/wiki/Light_curve) of [Type II supernovae](https://en.wikipedia.org/wiki/Type_II_supernova) (SNe II) during the first ~100 days. However, in principle, it can be applied to any set of data with one predictor variable, with or without errors on the response variable.

For any question, email me at olrodrig@gmail.com

**If you use the ALR in your work, please cite [Rodríguez et al. (2019)](https://ui.adsabs.harvard.edu/abs/2019MNRAS.483.5459R/abstract).**
