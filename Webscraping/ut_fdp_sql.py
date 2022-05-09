'''
Script is purely to digest csvs/ webscraping data into our databse
csv->df->sqltable
'''
import pandas as pd
import mysql.connector

#create a dataframe from the csv file mapping colummn name to index name
df = pd.read_csv('./ModdedfireDP.csv',encoding='latin-1')

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
    #row['...'] Follows the column title of  ModdedfireDP.csv.csv
    _streetAddr = str(row['Mail addr1'])
    _mailState = str(row['Mail state'])
    _city = str(row['Mail city'])

    #LocationAddr = str(_city[1]) + ', ' + str(_state[1]) + ', ' + str(_streetAddr[1])
    LocationAddr = _city + ', ' + _mailState + ', ' + _streetAddr
    print(LocationAddr)

    #Inserts newly created string into db
    sqls = "INSERT INTO defaultdb.Locations(LocationName, LocationAddr) VALUES (%s, %s)"
    val = ('Fire Department', LocationAddr)
    
    cursor.execute(sqls,val)
    connection.commit()
    

