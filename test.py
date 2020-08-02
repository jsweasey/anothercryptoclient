import json as json


portfolioToDisplay = 'User1'
with open('userholdings.json','r') as jsonToOpen:
    userCoinHoldingsJSON = json.load(jsonToOpen)

rowInsert = 0
columnInsert = 0
keys = userCoinHoldingsJSON[0].keys()
keyList = list(keys)
for v in range(len(keyList)):
    print(keyList[v])
