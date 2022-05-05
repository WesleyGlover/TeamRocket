'''
csv->df->list->sqltable
'''
import pandas as pd
import mysql.connector


df = pd.read_csv('./ModdedfireDP.csv',encoding='latin-1')

try:

    connection = mysql.connector.connect(
        user='doadmin',
        password ='AVNS_WZEScW_Y5FNKr7m',
        host='db-mysql-teamrocket-do-user-11106141-0.b.db.ondigitalocean.com',
        port = 25060,
        database='defaultdb'
    )

    cursor = connection.cursor()

except BaseException as e:
    print(str(e))



    
lst = []
for index,row in df.iterrows():
    _streetAddr = str(row['Mail addr1'])
    _mailState = str(row['Mail state'])
    _city = str(row['Mail city'])

    # LocationAddr = str(_city[1]) + ', ' + str(_state[1]) + ', ' + str(_streetAddr[1])
    LocationAddr = _city + ', ' + _mailState + ', ' + _streetAddr
    print(LocationAddr)

    sqls = "INSERT INTO defaultdb.Locations(LocationName, LocationAddr) VALUES (%s, %s)"
    val = ('Fire Department', LocationAddr)
    
    cursor.execute(sqls,val)
    connection.commit()
    

