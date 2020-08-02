import json as json
import requests
import api_service as api_service
import data_service as data_service
import tkinter as tk
import time as time
from datetime import datetime as datetime


class MainApp():

    #MAIN INITIALIZATION OF APP
    def __init__(self, master):
        self.master = master
        self.frameSecPrices = tk.Frame(self.master, borderwidth = 2, relief = 'sunken')
        self.frameApiConnectCheck = tk.Frame(self.master, borderwidth = 2, relief = 'sunken', padx = 300, pady = 10)

        self.labelUpdateTime = tk.Label(self.frameSecPrices, text = '')
        self.labelcoingeckoApiGet = tk.Label(self.frameSecPrices, text = '')
        self.labelcoingeckoApiCheck = tk.Label(self.frameApiConnectCheck, text = '')
        self.labelbinanceApiCheck = tk.Label(self.frameApiConnectCheck, text = '')


        self.frameSecPrices.pack(side = 'left')
        self.frameApiConnectCheck.pack(side = 'left')

        self.labelUpdateTime.pack()
        self.labelcoingeckoApiGet.pack()
        self.labelcoingeckoApiCheck.pack(side = 'left')
        self.labelbinanceApiCheck.pack(side = 'left')

        self.btcPriceSec()
        self.apiCheckSec()
        currentPortfolio = CoinHoldingsTable()
        currentPortfolio.createCoinHoldingsTableHeadings()
        currentPortfolio.createCoinHoldingsTable()
        currentPortfolio.pack(side = 'bottom')
        currentPortfolio.saveCoinHoldingsTable()

    def btcPriceSec(self):
        currentBtcPriceUSDJSON =  api_service.coingeckoApiGet('/simple/price', 'JSON', {'ids':'bitcoin','vs_currencies':'usd'})
        currentBtcPriceUSD = currentBtcPriceUSDJSON['bitcoin']['usd']
        self.labelcoingeckoApiGet.configure(text = 'BTC: $' + str(currentBtcPriceUSD))
        self.labelUpdateTime.configure(text = 'Last updated: ' + datetime.now().strftime('%H:%M:%S'))
        self.frameSecPrices.after(5000, self.btcPriceSec)

    def apiCheckSec(self):
        binanceApiResponse = api_service.binanceApiCheck()
        coingeckoApiResponse = api_service.coingeckoApiCheck()

        if binanceApiResponse[0] == True:
            self.labelbinanceApiCheck.configure(text = 'Binance API: Okay')
        else:
            self.labelbinanceApiCheck.configure(text = 'Binance API: Error ' + str(binanceApiResponse[1]))

        if coingeckoApiResponse[0] == True:
            self.labelcoingeckoApiCheck.configure(text = 'Coingecko API: Okay')
        else:
            self.labelcoingeckoApiCheck.configure(text = 'Coingecko API: Error' + str(coingeckoApiResponse[1]))
        self.frameApiConnectCheck.after(5000, self.apiCheckSec)



class CoinHoldingsTable(tk.Frame):

    def __init__(self):
        super(CoinHoldingsTable, self).__init__()
        self.frameUserCoinHoldings = tk.Frame(self, borderwidth = 2, relief = 'sunken')
        self.arrTableLabel = []
        self.arrTableData = {}

    def createCoinHoldingsTableHeadings(self):

        columnInsert = 0
        with open('userholdings.json','r') as jsonToOpen:
            userCoinHoldingsJSON = json.load(jsonToOpen)

        coinHoldingsKeys = userCoinHoldingsJSON[0].keys()
        listCoinHoldingsKeys = list(coinHoldingsKeys)
        for key in range(len(listCoinHoldingsKeys)):
            self.headingTableLabel = tk.Label(self, text = listCoinHoldingsKeys[key])
            self.headingTableLabel.grid(row = 0, column = columnInsert, padx = 1, pady = 1)
            columnInsert += 1

    def createCoinHoldingsTable(self):

        rowInsert = 1
        columnInsert = 0
        with open('userholdings.json','r') as jsonToOpen:
            userCoinHoldingsJSON = json.load(jsonToOpen)

        for coinIndex in (userCoinHoldingsJSON):
            columnInsert = 0
            currentRowLabel = []
            currentRowData = {}
            currentRowKeys = userCoinHoldingsJSON[(rowInsert - 1)].keys()
            currentRowKeysList = list(currentRowKeys)
            for coinData in coinIndex.values():
                self.tableLabel = tk.Label(self, text = coinData)
                self.tableLabel.grid(row = rowInsert, column = columnInsert, padx = 1, pady = 1)
                currentRowLabel.append(self.tableLabel)
                currentRowData.update({currentRowKeysList[columnInsert] : coinData})
                columnInsert += 1
            self.arrTableLabel.append(currentRowLabel)
            self.arrTableData.update(currentRowData)
            rowInsert += 1

    def saveCoinHoldingsTable(self):

        labelToChange = self.arrTableLabel[1][1]
        labelToChange.configure(text='egg')
        jsonArrTableData = json.dumps(self.arrTableData)
        print((jsonArrTableData))
        print('\n')
        with open('userholdings.json','r') as jsonToOpen:
            userCoinHoldingsJSON = json.load(jsonToOpen)
        print(userCoinHoldingsJSON)





def main():
    root = tk.Tk()
    MainApp(root)
    root.tk.mainloop()

if __name__ == '__main__':
    main()
