#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 15:57:18 2018

@author: warren
"""

# Import Libraries
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# Import dataset
data = pd.read_excel(io='Bloomberg Sample Data.xlsx', sheetname='Horizontal')

# Tidy Data

# Step 1: Observations should be rows and columns be variables
data_transpose = data.T

# Step 2: Convert to object as columns are not defined and we can pick out specific values
ds = data_transpose.values

# Step 3: Extract variables and observations from different companies
variables = ds[1,1:8].tolist()
variables.extend(["DATE", "COMPANY"])

dates = ds[2:,0]

g1_label = ds[1,0]
g1_data = ds[2:,1:8]

g2_label = ds[1,9]
g2_data = ds[2:,10:17]

g3_label = ds[1,18]
g3_data = ds[2:,19:26]

g4_label = ds[1,27]
g4_data = ds[2:,28:35]

g5_label = ds[1,36]
g5_data = ds[2:,37:44]

# Step 4: Construct data frame from company data groups
# Define helper functions
def preprocess_data_group(data, dates, company):
    N = data.shape[0]
    return np.c_[data, dates, np.repeat(company, N)]
    
def create_dataframe_from_data_group(data, variables):
    return pd.DataFrame(data=data, index=None, columns=[variables], dtype=None, copy=False)

# Step 4.1: Create dataframes for each company group
g1_data = preprocess_data_group(g1_data, dates, g1_label)
df_g1 = create_dataframe_from_data_group(g1_data, variables)

g2_data = preprocess_data_group(g2_data, dates, g2_label)
df_g2 = create_dataframe_from_data_group(g2_data, variables)

g3_data = preprocess_data_group(g3_data, dates, g3_label)
df_g3 = create_dataframe_from_data_group(g3_data, variables)

g4_data = preprocess_data_group(g4_data, dates, g4_label)
df_g4 = create_dataframe_from_data_group(g4_data, variables)

g5_data = preprocess_data_group(g5_data, dates, g5_label)
df_g5 = create_dataframe_from_data_group(g5_data, variables)

# Step 4.2: Concatenate company group dataframes
df = pd.concat([df_g1, df_g2, df_g3, df_g4, df_g5]).reset_index(drop=True)

# Step 5: Define variable types
vars_float = ["PX_LAST", "CURR_ENTP_VAL", "TRAIL_12M_EBITDA", "EBITDA_MARGIN", "PE_RATIO", "LT_DEBT_TO_COM_EQY", "DIVIDEND_YIELD"]
vars_date = ["DATE"]
vars_cat = ["COMPANY"]

df[vars_float] = df[vars_float].apply(pd.to_numeric, errors='ignore')
df[vars_date] = df[vars_date].apply(pd.to_datetime)
df[vars_cat] = df[vars_cat].apply(lambda x: x.astype('category'))

# Step 6: Seperate multiple observations types into seperate tables
df_a = df.filter(["DATE", "COMPANY", "PX_LAST", "CURR_ENTP_VAL", "PE_RATIO", "DIVIDEND_YIELD"])
df_b = df.filter(["DATE", "COMPANY", "LT_DEBT_TO_COM_EQY"])
df_c = df.filter(["DATE", "COMPANY", "TRAIL_12M_EBITDA", "EBITDA_MARGIN"])

# Step 7: Save cleaned data to csv
df_a.to_csv("cleaned_bloomberg_data.csv", encoding="utf-8")
df_b.to_csv("cleaned_bloomberg_data.csv", encoding="utf-8")
df_c.to_csv("cleaned_bloomberg_data.csv", encoding="utf-8")

# Examine data

df.describe()

df.apply(lambda x: sum(x.isnull()),axis=0)

# Missing values
df_a = df_a.dropna(subset=["CURR_ENTP_VAL", "PE_RATIO", "DIVIDEND_YIELD"])

sns.pointplot(x="DATE", y="PX_LAST", hue="COMPANY", data=df_a)
sns.pointplot(x="DATE", y="CURR_ENTP_VAL", hue="COMPANY", data=df_a)
sns.pointplot(x="DATE", y="TRAIL_12M_EBITDA", hue="COMPANY", data=df_c)
sns.pointplot(x="DATE", y="EBITDA_MARGIN", hue="COMPANY", data=df_c)
sns.pointplot(x="DATE", y="PE_RATIO", hue="COMPANY", data=df_a)
sns.pointplot(x="DATE", y="LT_DEBT_TO_COM_EQY", hue="COMPANY", data=df_b)
sns.pointplot(x="DATE", y="DIVIDEND_YIELD", hue="COMPANY", data=df_a)











