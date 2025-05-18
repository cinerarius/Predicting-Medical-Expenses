from urllib.request import urlretrieve
medical_expense = 'https://raw.githubusercontent.com/JovianML/opendatasets/master/data/medical-charges.csv'
urlretrieve(medical_expense, 'medical.csv')
import pandas as pd
medical_df = pd.read_csv('medical.csv')
medical_df.head()

medical_df.describe()

# Commented out IPython magic to ensure Python compatibility.
import math
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
# %matplotlib inline

fig_age = px.histogram(medical_df,
                       x='age',
                       marginal='box',
                       nbins = 47,
                       title='Distribution of Age')
fig_age.update_layout(bargap=0.1)
fig_age.show()

fig_age = px.histogram(medical_df,
                       x='bmi',
                       marginal='box',
                       color_discrete_sequence=['red'],
                       title='Distribution of BMI')
fig_age.update_layout(bargap=0.1)
fig_age.show()

fig_age = px.histogram(medical_df,
                       x='charges',
                       marginal='box',
                       color = 'smoker',
                       color_discrete_sequence=['green', 'grey'],
                       nbins = 47,
                       title='Distribution of Smoker and Non-Smoker')
fig_age.update_layout(bargap=0.1)
fig_age.show()

fig_age = px.histogram(medical_df,
                       x='charges',
                       marginal='box',
                       color = 'sex',
                       color_discrete_sequence=['brown', 'grey'],
                       nbins = 47,
                       title='Distribution by Sex')
fig_age.update_layout(bargap=0.1)
fig_age.show()

region_df = medical_df.groupby('region').agg({'charges':'mean'}).reset_index()
fig_region = plt.figure(figsize=(4,3))
axes_region = fig_region.add_axes([0,0,1,1])
axes_region.bar(region_df['region'], region_df['charges'], color='orange')

fig_age = px.histogram(medical_df,
                       x='smoker',
                       color = 'sex',
                       color_discrete_sequence=['grey', 'brown'],
                       title='Smoker')
fig_age.update_layout(bargap=0.1)
fig_age.show()

fig_age = px.scatter(medical_df,
                       x='age',
                       y='charges',
                       color= 'smoker',
                       opacity = 0.8,
                       hover_data=['sex'],
                       color_discrete_sequence=['green', 'red'],
                       title='Age vs Charges')
fig_age.update_layout(bargap=0.1)
fig_age.show()

fig_age = px.scatter(medical_df,
                       x='bmi',
                       y='charges',
                       color= 'smoker',
                       opacity = 0.8,
                       hover_data=['sex'],
                       color_discrete_sequence=['blue', 'orange'],
                       title='BMI vs Charges')
fig_age.update_layout(bargap=0.1)
fig_age.show()

px.violin(medical_df, x='children', y='charges', title='Children vs Charges')

#Correlation
medical_df.charges.corr(medical_df.age)

smoker_values = {'yes': 1, 'no': 0}
smoker_numeric = medical_df.smoker.map(smoker_values)
medical_df['smoker_num'] = smoker_numeric
sex_values = {'male': 1, 'female': 0}
sex_numeric = medical_df.sex.map(sex_values)
medical_df['sex_num'] = sex_numeric
medical_df.head()

medical_df[['age','bmi','children','smoker_num','sex_num','charges']].corr()

sns.heatmap(medical_df[['age','bmi','children','smoker_num','sex_num','charges']].corr(), cmap='Reds', annot=True)
plt.title('Correlation Heatmap')

#Trend Line - y = wx + b
'''w(slope) = rate of change of y with respect to x
   b(intercept) = value of y when x is 0'''
non_smoker_df = medical_df[medical_df.smoker == 'no']
px.scatter(medical_df, x='age', y='charges', color='sex')