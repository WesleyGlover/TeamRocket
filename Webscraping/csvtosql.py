'''
csv->df->list->sqltable
'''
import pandas as pd

df = pd.read_csv('../PLS_FY19_AE_pud19i.csv',encoding='latin-1')


lst = []
for index,row in df.iterrows():
    state = row['STABR']
    addr = row['ADDRESS']
    city = row['CITY']
    zipcode = row['CITY']

    string = addr + '/' + state + '/' + city

    lst.append(string)

print(lst)
