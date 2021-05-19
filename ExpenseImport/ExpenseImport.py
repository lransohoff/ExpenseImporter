# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 14:27:51 2019

@author: laure
"""

import pandas as pd
from datetime import datetime
import warnings

class ExpenseData:
    def __init__(self,source,account):
        self.source = source;
        self.dataset = [];
        self.columns = [];
        self.account = account;
        self.dataset;
        
    def import_expenses(self):
        df = pd.read_csv(self.source)
        ds = self.assign_columns(df);
        self.dataset = ds;
        date_col = ds.columns[0]
        des_col = ds.columns[1]
        datestr_array = [];
        mon_str_array = [];
        print(ds);
        for i in range(len(ds)):
            if len(ds[date_col][i]) < 10 and '/' in ds[date_col][i]:
                d = datetime.strptime(ds[date_col][i],"%m/%d/%y")
            elif '/' in ds[date_col][i]:
                d = datetime.strptime(ds[date_col][i],"%m/%d/%Y")
            elif '-' in ds[date_col][i]:
                d = datetime.strptime(ds[date_col][i],"%Y-%m-%d")
                
            else:
                print('Date format not recognized') 
#            print(d)        
            datestr_array.append(d.strftime("%m/%d/%Y"))
            mon_str_array.append(d.strftime("%b %Y"))
#        print(datestr_array)
        #self.dataset.insert(3,'Month',datestr_array)
        # Rename 'Date' column if needed
        print(ds);
        if date_col != 'Date':
#            self.dataset.insert(1,'Date',self.dataset[date_col])
            self.dataset.rename(columns = {date_col:'Date'}, inplace = True)
        # Reformat date column to '%m/%d/%y'
        #d_temp = self.dataset['Date']
        #self.dataset['Date'] = datetime.strftime(d_temp['Date'],"%m/%d/%y")
        self.dataset['Date'] = datestr_array
        # Rename 'Description' column if needed
        if des_col != 'Description':
            self.dataset.rename(columns = {des_col:'Description'}, inplace = True)
        # Add 'Account' column
        self.dataset.insert(3,'Account',[self.account] *len(df))
        # Clean Amount column and convert to float
        if df['Amount'].dtypes == 'str':
            self.dataset['Amount'] = self.dataset['Amount'].replace({'\$':''},regex=True)
            pd.to_numeric(self.dataset['Amount'], errors='coerce')
        self.columns = self.dataset.columns;
        print(ds);

        return self
    
    def append_expenses(self,expense_data_2):
        temp = pd.concat([self.dataset,expense_data_2.dataset]);
        self.dataset = temp;
        return self
        
    def sort_expenses(self,sort_column):
        #cols = self.dataset.columns;
        if sort_column in self.columns:
            self.dataset.sort_values(by=sort_column);
        else:
            warnings.warn('Sort column not in expenses dataframe')
        return self
    
    def write_expenses(self,file):
        #cols = self.dataset.columns;
        if 'Transaction Date' in self.columns:
            ds_to_write = self.dataset.drop('Transaction Date',axis=1)
        ds_to_write.to_excel(file)
        
    def assign_columns(self,df):
        cols = df.columns;
        date_col = '';
        des_col = '';
        amt_col = '';
        for c in range(len(cols)):
            if 'Date' in cols[c] and date_col == '':
                date_col = cols[c]
            elif 'Description' in cols[c] and des_col == '':
                des_col = cols[c]
            elif 'Merchant Name' in cols[c] and des_col == '':
                des_col = cols[c]
            elif 'Amount' in cols[c] and amt_col == '':
                amt_col = cols[c]
        df = df[[date_col, des_col, amt_col]]
        return df
