

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import KFold

name = ['jebucher']

# load data
data = pd.read_csv(r"C:\Users\jonat\GSE 524\data\boston.csv") 
y = data['MEDV']
x = data.drop("MEDV", axis = 1)

# model 1: linear regression using all 13 variables
model_1 = LinearRegression()
model_1.fit(x, y)

y_pred = model_1.predict(x)
mse_1 = mean_squared_error(y, y_pred)

# model 2: all 13 parameters and all interaction terms
poly = PolynomialFeatures(degree = 2, interaction_only = True, include_bias = False)
xp = pd.DataFrame(poly.fit_transform(x))
model_2 = LinearRegression(fit_intercept = False)
model_2.fit(xp, y)

y_pred = model_2.predict(xp)
mse_2 = mean_squared_error(y, y_pred)

# model 3: all interactions and quadratic term for all predictors
poly_sq = PolynomialFeatures(degree = 2, include_bias = True)
xps = pd.DataFrame(poly_sq.fit_transform(x))
model_3 = LinearRegression(fit_intercept = False)
model_3.fit(xps, y)

y_pred = model_3.predict(xps)
mse_3 = mean_squared_error(y, y_pred)

# model 4: log linear regression
log_y = np.log(y)
model_4 = LinearRegression()
model_4.fit(x, log_y)

y_pred = model_4.predict(x)
mse_4 = mean_squared_error(y, np.exp(y_pred))

# model 5: log linear regression with all 13 predictors and not all interactions
model_5 = LinearRegression(fit_intercept = False)
model_5.fit(xp, log_y)

y_pred = model_5.predict(xp)
mse_5 = mean_squared_error(y, np.exp(y_pred))

# model 6: log linear regression with all 13 predictors and interaction terms
model_6 = LinearRegression(fit_intercept = False)
model_6.fit(xps, log_y)

y_pred = model_6.predict(xps)
mse_6 = mean_squared_error(y, np.exp(y_pred))

# calculating bic values
bic_1 = len(data) * np.log(mse_1) + len(model_1.coef_) * np.log(len(data))
bic_2 = len(data) * np.log(mse_2) + len(model_2.coef_) * np.log(len(data))
bic_3 = len(data) * np.log(mse_3) + len(model_3.coef_) * np.log(len(data))
bic_4 = len(data) * np.log(mse_4) + len(model_4.coef_) * np.log(len(data))
bic_5 = len(data) * np.log(mse_5) + len(model_5.coef_) * np.log(len(data))
bic_6 = len(data) * np.log(mse_6) + len(model_6.coef_) * np.log(len(data))

bic = np.array([bic_1, bic_2, bic_3, bic_4, bic_5, bic_6])

# leave one out method
loo_1_scores = cross_val_score(LinearRegression(), x, y, cv = LeaveOneOut(),
                        scoring = "neg_mean_squared_error")
loo_1 = np.mean(loo_1_scores)

loo_2_scores = cross_val_score(LinearRegression(fit_intercept = False), xp, y, cv = LeaveOneOut(),
                        scoring = "neg_mean_squared_error")
loo_2 = np.mean(loo_2_scores)

loo_3_scores = cross_val_score(LinearRegression(fit_intercept = False), xps, y, cv = LeaveOneOut(),
                        scoring = "neg_mean_squared_error")
loo_3 = np.mean(loo_3_scores)

# how to do this with the log scores?
pred_l4 = cross_val_predict(LinearRegression(), x, log_y, cv = LeaveOneOut())
loo_4_scores = mean_squared_error(y, np.exp(pred_l4))
loo_4 = np.mean(loo_4_scores)

pred_l4 = cross_val_predict(LinearRegression(fit_intercept = False), xp, log_y, cv = LeaveOneOut())
loo_5_scores = mean_squared_error(y, np.exp(pred_l4))
loo_5 = np.mean(loo_5_scores)

pred_l6 = cross_val_predict(LinearRegression(fit_intercept = False), xps, log_y, cv = LeaveOneOut())
loo_6_scores = np.mean(pred_l6)
loo_6 = np.mean(loo_6_scores)

loo = np.array([loo_1, loo_2, loo_3, loo_4, loo_5, loo_6])


# k fold cross-validation,
k = 10 
scores_1 = cross_val_score(LinearRegression(), x, y, cv = KFold(k, shuffle = True, random_state = 0),
                         scoring = "neg_mean_squared_error")
mse_k1 = np.mean(scores_1)

scores_2 = cross_val_score(LinearRegression(fit_intercept = False), xp, y, cv = KFold(k, shuffle = True, random_state = 0),
                         scoring = "neg_mean_squared_error")
mse_k2 = np.mean(scores_2)

scores_3 = cross_val_score(LinearRegression(fit_intercept = False), xps, y, cv = KFold(k, shuffle = True, random_state = 0),
                         scoring = "neg_mean_squared_error")
mse_k3 = np.mean(scores_3)

pred_k4 = cross_val_predict(LinearRegression(), x, log_y, cv = KFold(k, shuffle = True, random_state = 0))
scores_4 = mean_squared_error(y, np.exp(pred_k4))
mse_k4 = np.mean(scores_4)

pred_k5 = cross_val_predict(LinearRegression(fit_intercept = False), xp, log_y, cv = KFold(k, shuffle = True, random_state = 0))
scores_5 = mean_squared_error(y, np.exp(pred_k5))
mse_k5 = np.mean(scores_5)

pred_k6 = cross_val_predict(LinearRegression(fit_intercept = False), xps, log_y, cv = KFold(k, shuffle = True, random_state = 0))
scores_6 = mean_squared_error(y, np.exp(pred_k6))
mse_k6 = np.mean(scores_6)

kfold = np.array([mse_k1, mse_k2, mse_k3, mse_k4, mse_k5, mse_k6])

kfold = np.abs(kfold)
loo = np.abs(loo)
bic = np.abs(bic)

# choosing the best model by each criteria
best_bic = np.argmin(bic) + 1
best_loo = np.argmin(loo) + 1
best_kfold = np.argmin(kfold) + 1

print(bic)
print(loo)
print(kfold)

print(best_bic, best_loo, best_kfold)
