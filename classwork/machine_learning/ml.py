
import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor



name = ['jebucher']

# load data
data = pd.read_csv(r"C:\Users\jonat\GSE 524\data\boston.csv") 
y = data['MEDV']
x = data.drop("MEDV", axis = 1)

# (7) decision tree
model_7 = DecisionTreeRegressor(criterion = "squared_error", random_state = 0)
model_7.fit(x, y)

k = 10 
scores_7 = cross_val_score(DecisionTreeRegressor(criterion = "squared_error", random_state = 0), x, y, cv = KFold(k, shuffle = True, random_state = 0),
                         scoring = "neg_mean_squared_error")
mse_k7 = np.mean(scores_7)

# (8) small decision tree (10 obs)
model_8 = DecisionTreeRegressor(criterion = "squared_error", min_samples_leaf = 10, random_state = 0)
model_8.fit(x, y)

scores_8 = cross_val_score(DecisionTreeRegressor(criterion = "squared_error", min_samples_leaf = 10, random_state = 0), x, y, cv = KFold(k, shuffle = True, random_state = 0),
                         scoring = "neg_mean_squared_error")
mse_k8 = np.mean(scores_8)

# (9) random forest model with 100 trees

model_9 = RandomForestRegressor(criterion = "squared_error", n_estimators = 100, random_state = 0)
model_9.fit(x, y)

scores_9 = cross_val_score(RandomForestRegressor(criterion = "squared_error", n_estimators = 100, random_state = 0), x, y, cv = KFold(k, shuffle = True, random_state = 0),
                         scoring = "neg_mean_squared_error")
mse_k9 = np.mean(scores_9)

# (10)

model_10 = RandomForestRegressor(criterion = "squared_error", n_estimators = 100, max_features = 1/3, random_state = 0)
model_10.fit(x, y)

scores_10 = cross_val_score(RandomForestRegressor(criterion = "squared_error", n_estimators = 100, max_features = 1/3, random_state = 0), x, y, cv = KFold(k, shuffle = True, random_state = 0),
                         scoring = "neg_mean_squared_error")
mse_k10 = np.mean(scores_10)

kfold = np.array([mse_k7, mse_k8, mse_k9, mse_k10])
kfold = np.abs(kfold)

best_tree = np.argmin(kfold) + 7

best_overall = 10

yhat = model_10.predict(x)
