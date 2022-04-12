from ctypes import sizeof
from re import M
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import mysql.connector
import pandas as pd


url = f"https://locations.quiktrip.com/"  #main page for qt locations. Displays every state that have qt locations

page = requests.get(url).text  #gets the html of the main page
doc = BeautifulSoup(page, "html.parser")    #gives the html of the main page to BeautifulSoup parser

statesPage = doc.find_all(class_="Directory-listLinkText")  
statesPage = str(statesPage).split(",")

stateList = []

#finds the states in the html of the main page
for i in range(len(statesPage) - 1) :
    stateList.append(str(statesPage[i]).split(">")[-2].split("<")[0])

#matches the states found to the list of touples that have the corrosponding state abbreviation
stateAbList = []
stateTuple = [("al","Alabama"),("ak","Alaska"),("az","Arizona"),("ar","Arkansas"),("ca", "California"),("co", "Colorado"),("ct","Connecticut"),("dc","Washington DC"),("de","Delaware"),("fl","Florida"),("ga","Georgia"),("hi","Hawaii"),("id","Idaho"),("il","Illinois"),("in","Indiana"),("ia","Iowa"),("ks","Kansas"),("ky","Kentucky"),("la","Louisiana"),("me","Maine"),("md","Maryland"),("ma","Massachusetts"),("mi","Michigan"),("mn","Minnesota"),("ms","Mississippi"),("mo","Missouri"),("mt","Montana"),("ne","Nebraska"),("nv","Nevada"),("nh","New Hampshire"),("nj","New Jersey"),("nm","New Mexico"),("ny","New York"),("nc","North Carolina"),("nd","North Dakota"),("oh","Ohio"),("ok","Oklahoma"),("or","Oregon"),("pa","Pennsylvania"),("ri","Rhode Island"),("sc","South Carolina"),("sd","South Dakota"),("tn","Tennessee"),("tx","Texas"),("ut","Utah"),("vt","Vermont"),("va","Virginia"),("wa","Washington"),("wv","West Virginia"),("wi","Wisconsin"),("wy","Wyoming")]

for j in range(len(stateTuple)):
    for i in range(len(statesPage) - 1):
        if(stateList[i] in stateTuple[j]):
            stateAbList.append(stateTuple[j][0])
            
cityNState = [] #list of cities and states that have qt locations in them
qtAdd = [] 
combAdd = [] #final list of qt locations with format: ['1234 Five ave/tx/denton', '6789 Ten Blvd/tx/dallas']

#Feed the states abbreviations into the url to get to that states page
#To make this search every state for qt locations replace range(2): with range(0,len(stateAbList)) and {stateAbList[2]} with {stateAbList[i]}

for i in range(12,14):
    StateUrl = f"https://locations.quiktrip.com/{stateAbList[i]}"
    page = requests.get(StateUrl).text
    doc = BeautifulSoup(page, "html.parser")
    cities = doc.find_all(class_="Directory-listLink")
    cities = str(cities).split("\"")

#Find every city in each state and format it to fit the right url
    for j in range(len(cities) - 1) :
        if " href=" in cities[j]:
            temp = str(cities[j+1]).split("/")

            if(len(temp) == 3):
                tempStr = '/'.join(temp[:-1])
            else:
                tempStr = '/'.join(temp)

            cityNState.append(tempStr)

#Go to each cities url and pull the addresses of the qt locations in that particular city
            for k in range(len(cityNState)):
                cityUrl = f"https://locations.quiktrip.com/{cityNState[k]}"
                page = requests.get(cityUrl).text
                doc = BeautifulSoup(page, "html.parser")
                citiesAdd = doc.find_all(class_="c-AddressRow")
                citiesAdd = str(citiesAdd).split(">")

#Checks to make sure there are no duplicates in the list of qt locations
                for r in range(len(citiesAdd)):
                    if citiesAdd[r] == "<span class=\"c-address-street-1\"" and qtAdd.__contains__(citiesAdd[r+1]) == False and qtAdd.__contains__(citiesAdd[r+1][:-6]) == False:
                        qtAdd.append(citiesAdd[r+1][:-6])         
                        qtAdd.append(cityNState[k])

#Appends the city and state to the qt address  
                        for t in range(0, len(qtAdd), 2):
                            combAdd.append(qtAdd[t] + "/" + qtAdd[t+1])
                        
                combAdd = list(dict.fromkeys(combAdd))


try:

    connection = mysql.connector.connect(
        user='doadmin',
        password ='AVNS_WZEScW_Y5FNKr7m',
        host='db-mysql-teamrocket-do-user-11106141-0.b.db.ondigitalocean.com',
        port = 25060,
        database='defaultdb'
    )

    cursor = connection.cursor()
    #cursor.execute("Select * From Location")
    #result = cursor.fetchall()
    #print(result)
    
except BaseException as e:
    print(str(e))

for i in combAdd:
    lst = []
    lst.append(i)

    
    sqls = "INSERT INTO defaultdb.Location VALUES (%s)"
    cursor.execute(sqls,lst)
    connection.commit()



'''
Dataframe example (Prob not needed)

lst = []
newlst = []
x = 0
for i in combAdd:
    x+=1
    lst = [x,i]
    newlst.append(lst)
    
df = pd.DataFrame(newlst, columns=['LocationID','Location'])
'''

    
