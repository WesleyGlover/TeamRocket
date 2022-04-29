import random
import csv


fireDP = list(csv.reader(open("fireDepartments.csv")))

print(fireDP[1][3])

for i in range(1, len(fireDP) - 1):
    if(fireDP[i][7] == "" and fireDP[i][10] != ""):
        fireDP[i][7] = fireDP[i][9]
    elif(fireDP[i][7] == "" and fireDP[i][10] == "" and fireDP[i][2] != ""):
        fireDP[i][7] = fireDP[i][2]
        fireDP[i][8] = fireDP[i][3]
    elif(fireDP[i][7] == "" and fireDP[i][10] == "" and fireDP[i][2] == ""):
        fireDP[i].pop()

fields = ['FDID', 'Fire dept name', 'HQ addr1', 'HQ addr2', 'HQ city', 'HQ state', 'HQ zip', 'Mail addr1', 'Mail addr2', 'Mail PO box', 'Mail city', 'Mail state', 'Mail zip', 'HQ phone', 'HQ fax', 'County', 'Organization Type', 'Number Of Stations', 'Active Firefighters - Volunteer', 'Non-Firefighting - Civilian', 'Primary agency for emergency mgmt']

with open('trimmedFireDP.csv', 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(fireDP)