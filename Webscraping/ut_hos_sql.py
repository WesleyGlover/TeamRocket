'''
Script is purely to digest csvs/ webscraping data into our databse
csv->df->sqltable
'''
import pandas as pd
import mysql.connector

#create a dataframe from the csv file mapping colummn name to index name
df = pd.read_csv('./hospitals.csv',encoding='latin-1')

try:
    #Authentication
    connection = mysql.connector.connect(
        user='doadmin',
        password ='AVNS_WZEScW_Y5FNKr7m',
        host='db-mysql-teamrocket-do-user-11106141-0.b.db.ondigitalocean.com',
        port = 25060,
        database='defaultdb'
    )
    #cursor handles queries to the db
    cursor = connection.cursor()

except BaseException as e:
    print(str(e))

for index,row in df.iterrows():

    #Acceptable address to latlon glendale, az, 5082 NW Grand Ave -> city, state, street address;
    #Grab the city state and street address from the original string
    #row['...'] Follows the column title of  PLS_FY19_Outlet_pud19i.csv
    _streetAddr = str(row['ADDRESS'])
    _mailState = str(row['STATE'])
    _Latitiude = str(row['LATITUDE'])
    _Longtitude = str(row['LONGITUDE'])
    _city = str(row['CITY'])

    #Proper Address Format
    LocationAddr = _city + ', ' + _mailState + ', ' + _streetAddr
    print(LocationAddr)

    #Inserts LocationAddr into the table Locations
    sqls = "INSERT INTO defaultdb.Locations(LocationName, LocationAddr, LocationLong, LocationLat) VALUES (%s, %s,%s,%s)"
    val = ('Hospital', LocationAddr, _Longtitude, _Latitiude)

    #Execute insert statement then commit it to the db
    cursor.execute(sqls,val)
    connection.commit()

