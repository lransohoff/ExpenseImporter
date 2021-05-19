# -*- coding: utf-8 -*-
# Header

import os
import pandas as pd
from ExpenseImport.ExpenseImport import ExpenseData

def run():
    # Import all expenses in the Temp folder, put them together and write to file
    base_path = os.getcwd()
    statement_path = base_path + '\\Statements'
    files = os.listdir(statement_path)
    out_file = base_path + '\\Results' + '\\' + 'output.csv'
    format_file = base_path + '\\statement_formats_example.csv'
    format_df = pd.read_csv(format_file)
    e = []
    ds_list = []
    for i in range(len(files)):
        found_file = False
        j = 0
        account = 'N/A'
        while not found_file and j <= len(format_df) - 1:
            if files[i].find(format_df['Account Name'][j]) >= 0:
                account = format_df['Account Name'][j]
            j += 1
        if files[i].find('.') >= 0: #Ignore Last Month folder in this directory
            e.append(ExpenseData(statement_path + '\\' + files[i], account))
            e[i].import_expenses()
            print(e[i].columns)
            ds_list.append(e[i].dataset)
    
    all_expenses = pd.concat(ds_list)
    all_expenses.to_csv(out_file)
    
if __name__ == '__main__':
    run()