# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 17:53:37 2019

@author: Data Quezt
"""


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sklearn import preprocessing
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression

plt.rc("font", size=14)
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

closed_list = []
unclosed_list = []
data = open('closed_list.txt').read().split('\n')
for x in range(1, len(data)):
    closed = unclosed = ''
    if len(data[x].split(' ')) == 2:
        closed, unclosed = data[x].split(' ');
        closed_list.append(int(closed))
        unclosed_list.append(int(unclosed))
    else:
        closed = data[x].split(' ')[0]
        closed_list.append(int(closed))

closed_list = set(closed_list)
unclosed_list = set(unclosed_list)

# Exploring and cleaning the data

csv_customer_market_dim = pd.read_csv('Cust&MarketDim.txt', delimiter=',')
csv_customer_market_dim.dropna(subset=["id"], inplace=True)
csv_customer_market_dim = csv_customer_market_dim.drop_duplicates("id")


sas_data_expert_industry_grading = pd.read_csv('industry_grade.csv', delimiter=",")
sas_data_expert_industry_grading.dropna(subset=["id"], inplace=True)
sas_data_expert_industry_grading = sas_data_expert_industry_grading.drop_duplicates("id")


csv_data_fin_hr_dim = pd.read_csv('Fin&HRDIM.csv', delimiter=',')
csv_data_fin_hr_dim.dropna(subset=["id"], inplace=True)
csv_data_fin_hr_dim = csv_data_fin_hr_dim.drop_duplicates("id")


xls_data_initial_investment = pd.read_excel('IntialInvestmentDetails.xlsx')
xls_data_initial_investment.dropna(subset=["id"], inplace=True)
xls_data_initial_investment = xls_data_initial_investment.drop_duplicates("id")

csv_manage_strategic_dim = pd.read_csv('Manage&StrategicDim.txt', delimiter='\t')
csv_manage_strategic_dim.dropna(subset=["id"], inplace=True)
csv_manage_strategic_dim = csv_manage_strategic_dim.drop_duplicates("id")

sas_data_opdim = pd.read_sas('opdim.sas7bdat')
sas_data_opdim.dropna(subset=["id"], inplace=True)
sas_data_opdim = sas_data_opdim.drop_duplicates("id")

csv_start_year = pd.read_csv('StartYearInfo.txt', delimiter=' ')
csv_start_year.dropna(subset=["id"], inplace=True)
csv_start_year = csv_start_year.drop_duplicates("id")

csv_data_vertical_location = pd.read_csv('Vertical&Location.txt', delimiter='\t')
csv_data_vertical_location.dropna(subset=["id"], inplace=True)
csv_data_vertical_location = csv_data_vertical_location.drop_duplicates("id")

data = csv_start_year.merge(xls_data_initial_investment,"outer", on=["id"])
data = data.merge(csv_data_vertical_location, 'outer' ,on = 'id')
data = data.merge(sas_data_opdim, "outer", on = "id")
data = data.merge(sas_data_expert_industry_grading, "outer" , on="id")
data = data.merge(csv_customer_market_dim, "outer" , on = "id")
data = data.merge(csv_manage_strategic_dim, "outer", on="id")
data = data.merge(csv_data_fin_hr_dim, "outer", on="id")

status = pd.Series([]);
for i in range(len(data)):
    if int(data["id"][i]) in closed_list:
        status[i] = 0
    if int(data["id"][i]) in unclosed_list:
        status[i] = 1

data.insert(17, 'status', status)

data.to_csv('dataset.csv',index=False)

null_columns = data.columns[data.isnull().any()]
null_status = data[data["status"].isnull()]

null_status.to_csv('null-status.csv', index=False)

data.dropna(subset=["year"], inplace=True)

# Replace missing numerical values with mean
data = data.fillna(data.mean())

data_summary = data.describe()
data_summary.to_csv('summary.csv', index=False)
print(data_summary)

# Analysing data

print(data["status"].value_counts())
sns.countplot(x='status', data=data, palette='hls')
plt.show()

count_of_still_running_startups = len(data[data['status']==1])
count_of_closed_startups = len(data[data['status']==0])
per_of_running_startups = count_of_still_running_startups / len(data)
per_of_closed_startups = count_of_closed_startups / len(data)

print("Total no of startups still running : ", count_of_still_running_startups)
print("Total no of startups that failed: ", count_of_closed_startups)
print("Percentage of startup still running: ", round(per_of_running_startups * 100, 2))
print("Percentage of startup that failed: ", round(per_of_closed_startups * 100))

print("\n\nMean related to status of startups\n")
print(data.groupby('status').mean())

print("\n\nMean related to Customer Dimension of startups\n")
print(data.groupby('CustomerDimension').mean())

print("\n\nMean related to Market Dimension of startups\n")
print(data.groupby('MarketDimension').mean())

pd.crosstab(data.MarketDimension, data.status).plot(kind='bar')
plt.title('Success frequency for Market Dimension')
plt.xlabel('Market Dimesion')
plt.ylabel('No of Companies')
plt.savefig('Market and Customer Dimesion')

pd.crosstab(data.CustomerDimension, data.status).plot(kind='bar')
plt.title('Success frequency for Customer Dimension')
plt.xlabel('Customer Dimesion')
plt.ylabel('No of Companies')
plt.savefig('Market and Customer Dimesion')
#
#plt.figure()
#data.plot()
#
#plt.figure()
#data.hist()
#
#plt.figure()
#data.plot.barh()

data.plot.scatter(x='status', y='HRDimension')