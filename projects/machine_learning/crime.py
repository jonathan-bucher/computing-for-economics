
import numpy as np
import pandas as pd
import statsmodels.formula.api as sm

# name
name = ['jebucher']

# load that data
fulldata = pd.read_csv(r"C:\Users\jonat\GSE 524\data\london_crime.csv")

# part 1
# add in a crimerate column
fulldata['crimerate'] = fulldata['crime'] / fulldata['population']

# add in a policerate column
fulldata['policerate'] = fulldata['police'] / fulldata['population']

# log-log specification
fulldata['lcrime'] = np.log(fulldata['crimerate'])
fulldata['lpolice'] = np.log(fulldata['policerate'])
fulldata['lemp'] = np.log(fulldata['emp'])
fulldata['lun'] = np.log(fulldata['un'])
fulldata['lymale'] = np.log(fulldata['ymale'])
fulldata['lwhite'] = np.log(fulldata['white'])

# create model
model1 = sm.ols("lcrime ~ lpolice + lemp + lun + lymale + lwhite", 
                data = fulldata).fit()


# part 2

# create upper and lower half dataframes to create weekly differences
lower = fulldata.loc[fulldata['week'] < 53]
upper = fulldata.loc[fulldata['week'] > 52]

lower.reset_index(inplace = True)
upper.reset_index(inplace = True)

# create diffdata dataframe
diffdata = pd.DataFrame()

# create the differenced data
diffdata['dlcrime'] = upper['lcrime'] - lower['lcrime']
diffdata['dlpolice'] = upper['lpolice'] - lower['lpolice']
diffdata['dlun'] = upper['lun'] - lower['lun']
diffdata['dlemp'] = upper['lemp'] - lower['lemp']
diffdata['dlymale'] = upper['lymale'] - lower['lymale']
diffdata['dlwhite'] = upper['lwhite'] - lower['lwhite']

# add in a week column
diffdata['week'] = lower['week'].copy()
diffdata['borough'] = upper['borough'].copy()

# model on differenced effects including fixed effects
model2 = sm.ols("dlcrime ~ dlpolice + dlun + dlemp + dlymale + dlwhite + C(week)",
                data = diffdata).fit()


# part 3
# reverse regression effects

# create first dummy variable 1's for weeks 80-85, 0 otherwise
diffdata['sixweeks'] = (28 <= diffdata['week']) & (diffdata['week'] <= 33)

diffdata['sixweeks'] = diffdata['sixweeks'].astype(int)

# create second dummy variable, 1's for weeks 80-85
# in the six boroughs of interest, 0 otherwise

diffdata['sixweeks_treat'] = (diffdata['borough'] < 4) | (diffdata['borough'] == 6) | (diffdata['borough'] == 14)

diffdata['sixweeks_treat'] = diffdata['sixweeks_treat'] * diffdata['sixweeks'].copy()

diffdata['sixweeks_treat'] = diffdata['sixweeks_treat'].astype(int)

# create model
model3 = sm.ols(
    'dlcrime ~ dlemp + dlpolice + dlun + dlymale + dlwhite + C(sixweeks) + C(sixweeks_treat)', 
    data = diffdata).fit()



