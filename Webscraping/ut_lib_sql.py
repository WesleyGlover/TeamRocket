'''
Script is purely to digest csvs/ webscraping data into our databse
csv->df->sqltable
'''
import pandas as pd
import mysql.connector

#create a dataframe from the csv file mapping colummn name to index name
df = pd.read_csv('./PLS_FY19_Outlet_pud19i.csv',encoding='latin-1')

try:
    #Authentication
    connection = mysql.connector.connect(
        user='doadmin',
        password ='AVNS_WZEScW_Y5FNKr7m',
        host='db-mysql-teamrocket-do-user-11106141-0.b.db.ondigitalocean.com',
        port = 25060,
        database='defaultdb'
    )
    #cursor handles all sql queries
    cursor = connection.cursor()

except BaseException as e:
    print(str(e))

for index,row in df.iterrows():

    #Acceptable address to latlon glendale, az, 5082 NW Grand Ave -> city, state, street address;
    #Grab the city state and street address from the original string
    #row['...'] Follows the column title of  PLS_FY19_Outlet_pud19i.csv
    _streetAddr = str(row['ADDRESS'])
    _mailState = str(row['STABR'])
    _city = str(row['CITY'])


    #Proper Address Format
    LocationAddr = _city + ', ' + _mailState + ', ' + _streetAddr
    print(LocationAddr)

    #Insert into DB
    sqls = "INSERT INTO defaultdb.Locations(LocationName, LocationAddr) VALUES (%s, %s)"
    val = ('Public Library', LocationAddr)

    #Execute SQL query and commit it to db
    cursor.execute(sqls,val)
    connection.commit()

