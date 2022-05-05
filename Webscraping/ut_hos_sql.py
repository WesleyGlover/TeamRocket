'''
csv->df->list->sqltable
'''
import pandas as pd
import mysql.connector


df = pd.read_csv('./hospitals.csv',encoding='latin-1')

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
    _streetAddr = str(row['ADDRESS'])
    _mailState = str(row['STATE'])
    _Latitiude = str(row['LATITUDE'])
    _Longtitude = str(row['LONGITUDE'])
    _city = str(row['CITY'])

    # LocationAddr = str(_city[1]) + ', ' + str(_state[1]) + ', ' + str(_streetAddr[1])
    LocationAddr = _city + ', ' + _mailState + ', ' + _streetAddr
    print(LocationAddr)

    sqls = "INSERT INTO defaultdb.Locations(LocationName, LocationAddr, LocationLong, LocationLat) VALUES (%s, %s,%s,%s)"
    val = ('Hospital', LocationAddr, _Longtitude, _Latitiude)
    
    cursor.execute(sqls,val)
    connection.commit()

