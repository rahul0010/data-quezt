# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels as sm
from sklearn import preprocessing
import matplotlib.pyplot as plt
plt.rc("font", size=14)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

#
#closed = []
#still_open = []
#file = pd.read_csv('closed_list.txt',delimiter=' ')
#
#for x in file.iteritems():
#    for j in range(0,len(x[0][1])):
#        closed.append(x[0][1][j])


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
        

csv_customer_market_dim = pd.read_csv('Cust&MarketDim.txt', delimiter=',')
sas_data_expert_industry_grading = pd.read_csv('industry_grade.csv', delimiter=",")
csv_data_fin_hr_dim = pd.read_csv('Fin&HRDIM.csv', delimiter=',')
xls_data_initial_investment = pd.read_excel('IntialInvestmentDetails.xlsx')
csv_manage_strategic_dim = pd.read_csv('Manage&StrategicDim.txt', delimiter='\t')
sas_data_opdim = pd.read_sas('opdim.sas7bdat')
csv_start_year = pd.read_csv('StartYearInfo.txt', delimiter=' ')
csv_data_vertical_location = pd.read_csv('Vertical&Location.txt', delimiter='\t')

data = csv_start_year.merge(xls_data_initial_investment, 'outer', on='id')
data = data.merge(csv_data_vertical_location, 'outer', on='id')
data = data.merge(sas_data_opdim,'outer', on='id')
data = data.merge(sas_data_expert_industry_grading, 'outer', on='id')
data = data.merge(csv_customer_market_dim, 'outer', on='id')
data = data.merge(csv_manage_strategic_dim, 'outer', on='id')
data = data.merge(csv_data_fin_hr_dim, 'outer', on='id')


# removing nan id's from csv_customer_market_dim
data.dropna(subset=["id"], inplace=True)

status = pd.Series([]);
for i in range(len(data)):
    if int(data["id"][i]) in closed_list:
        status[i] = 0
    if int(data["id"][i]) in unclosed_list:
        status[i] = 1

data.insert(17, 'status', status)

# removing nan status rows
data.dropna(subset=["id"], inplace=True)

# Analysing customer market dimension
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
print(csv_customer_market_dim.groupby('status').mean())

print("\n\nMean related to Customer Dimension of startups\n")
print(csv_customer_market_dim.groupby('CustomerDimension').mean())

print("\n\nMean related to Market Dimension of startups\n")
print(csv_customer_market_dim.groupby('MarketDimension').mean())

pd.crosstab(csv_customer_market_dim.MarketDimension, csv_customer_market_dim.status).plot(kind='bar')
plt.title('Success frequency for Market Dimension')
plt.xlabel('Market Dimesion')
plt.ylabel('Sucess')
plt.savefig('Market and Customer Dimesion')

pd.crosstab(csv_customer_market_dim.CustomerDimension, csv_customer_market_dim.status).plot(kind='bar')
plt.title('Success frequency for Customer Dimension')
plt.xlabel('Customer Dimesion')
plt.ylabel('Sucess')
plt.savefig('Market and Customer Dimesion')