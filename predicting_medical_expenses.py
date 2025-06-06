# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import math
from urllib.request import urlretrieve
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
# %matplotlib inline

medical_expense = 'https://raw.githubusercontent.com/JovianML/opendatasets/master/data/medical-charges.csv'
urlretrieve(medical_expense, 'medical.csv')
medical_df = pd.read_csv('medical.csv')
medical_df.head()

def estimate_charges(age, w, b):
  return w * age + b
estimated_charges = estimate_charges(medical_df.age, 267.24891283, -2091.4205565650864)
estimated_charges.head()

non_smoker_df = medical_df[medical_df.smoker == 'no']

#residual = predicted - actual
predicted_value = estimated_charges
target_charges = non_smoker_df.charges
residual = predicted_value - target_charges
residual.head()

def rmse(targets, predictions):
  return np.sqrt(np.mean(np.square(targets - predictions)))
targets = non_smoker_df.charges
rmse(targets, estimated_charges)

ages = non_smoker_df.age
charges = non_smoker_df.charges
def try_parameter(w, b):
  estimated_charges = estimate_charges(ages, w, b)
  targets = non_smoker_df.charges
  fig_charges = plt.figure(figsize=(8,6))
  axes_charges = fig_charges.add_axes([0,0,1,1])
  axes_charges.scatter(ages, charges, color='orange')
  axes_charges.plot(ages, estimated_charges, color='red')
  plt.xlabel('Age')
  plt.ylabel('Charges')
  plt.title('Age vs Charges')
  return rmse(targets, estimated_charges)

try_parameter(267.24891283, -2091.4205565650864)

model = LinearRegression()
help(model.fit)

#Ordinary Least Square(Small Dataset)
#Stochastic Gradient Descent(Larger Dataset)
input = non_smoker_df[['age']]
target = non_smoker_df.charges
print('Input shape:', input.shape)
print('Target shape:', target.shape)

model.fit(input, target)

predictions = model.predict(input)
predictions, target

rmse(target, predictions)

print('Predicted w: ', model.coef_)
print('Predicted b: ', model.intercept_)

model_sgd = SGDRegressor()
model_sgd.fit(input, target)

model_sgd.predict(input)
model_sgd.coef_, model_sgd.intercept_

try_parameter(model_sgd.coef_, model_sgd.intercept_)

inputs, targets = non_smoker_df[['age', 'bmi', 'children']], non_smoker_df['charges']
model = LinearRegression().fit(inputs, targets)
predictions = model.predict(inputs)
loss = rmse(targets, predictions)
print('Loss: ',loss)
print('Predicted w1, w2, w3: ',model.coef_)
print('Predicted b: ',model.intercept_)

'''
Categorical Data
#1 Two Categories: 0 and 1
#2 More Tnan Two Category: One-Hot Encoding
#3 Natural Order: Ordinal Encoding
'''
sns.barplot(x='smoker', y='charges', data=medical_df)

#Smoker Code
smoker_code = {'yes': 1, 'no': 0}
medical_df['smoker_code'] = medical_df.smoker.map(smoker_code)
#Sex Code
sex_code = {'male': 1, 'female': 0}
medical_df['sex_code'] = medical_df.sex.map(sex_code)
#Heatmap
sns.heatmap(medical_df[['charges','age','smoker_code','bmi', 'sex_code','children']].corr(), cmap='Reds', annot=True)

from sklearn import preprocessing
enc = preprocessing.OneHotEncoder()
enc.fit(medical_df[['region']])
enc.categories_
#One-Hot Encoding
one_hot = enc.transform(medical_df[['region']]).toarray()
one_hot
medical_df[['northeast', 'northwest', 'southeast', 'southwest']] = one_hot
medical_df.head()

inputs, targets = medical_df[['age', 'bmi', 'children', 'smoker_code', 'sex_code',
                              'northeast', 'northwest', 'southeast', 'southwest']], medical_df['charges']
model_final = LinearRegression().fit(inputs, targets)
predictions = model_final.predict(inputs)
loss = rmse(targets, predictions)
print('Loss: ', loss)
print('Predicted w: ', model.coef_)
print('Predicted b: ', model.intercept_)
new_customer = [[19, 27.9, 0, 1, 0, 1, 0, 0, 0]]
print('Charges will be: ', model_final.predict(new_customer))

weight_df = pd.DataFrame({
    'Variable': ['age', 'bmi', 'children', 'smoker_code', 'sex_code',
                              'northeast', 'northwest', 'southeast', 'southwest'],
    'Weight': model_final.coef_
})
weight_df

'''Optimization and Standardization'''
from sklearn.preprocessing import StandardScaler
numeric_columns = ['age', 'bmi', 'children']
scaler = StandardScaler()
scaler.fit(medical_df[numeric_columns])

scaler.mean_

scaler.var_

scaled_inputs = scaler.transform(medical_df[numeric_columns])
scaled_inputs

cat_col = ['smoker_code','sex_code', 'northeast', 'northwest', 'southeast', 'southwest']
categorical_data = medical_df[cat_col].values
categorical_data

inputs = np.concatenate((scaled_inputs, categorical_data), axis=1)
target = medical_df.charges
model = LinearRegression().fit(inputs, target) #Training the Model
predictions = model.predict(inputs) #Generating Prediction
loss = rmse(target, predictions) #Computing Loss
print('Loss: ', loss)
print('Predicted w: ', model.coef_)
print('Predicted b: ', model.intercept_)

import numpy as np
weight_df = pd.DataFrame({
    'Variable': np.append(numeric_columns + cat_col, 1),
    'Weight': np.append(model.coef_, model.intercept_)
})
weight_df.sort_values('Weight', ascending=False)

new_customer = [[19, 27.9, 0, 1, 0, 1, 0, 0, 0]]
scaler.transform([[19, 27.9, 0]])

new_customer_scaled = [[-1.43876426, -0.45332, -0.90861367, 1, 0, 1, 0, 0, 0]]
model.predict(new_customer_scaled)