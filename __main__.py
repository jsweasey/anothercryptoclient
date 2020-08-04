import json as json
import requests as requests
import api_service as api_service
import data_service as data_service
import tkinter as tk
import time as time
import os as os
from datetime import datetime as datetime


class MainApp():

    #MAIN INITIALIZATION OF APP
    def __init__(self, master):
        self.master = master
        self.frameSecPrices = tk.Frame(self.master, borderwidth = 2, relief = 'sunken')
        self.frameApiConnectCheck = tk.Frame(self.master, borderwidth = 2, relief = 'sunken', padx = 300, pady = 10)
        self.frameCoinHoldings = tk.Frame(self.master, borderwidth = 2, relief = 'sunken')

        self.labelUpdateTime = tk.Label(self.frameSecPrices, text = '')
        self.labelcoingeckoApiGet = tk.Label(self.frameSecPrices, text = '')
        self.labelcoingeckoApiCheck = tk.Label(self.frameApiConnectCheck, text = '')
        self.labelbinanceApiCheck = tk.Label(self.frameApiConnectCheck, text = '')


        self.frameSecPrices.grid(row = 0, column = 0)
        self.frameApiConnectCheck.grid(row = 0, column = 1)
        self.frameCoinHoldings.grid(row = 1, column = 1)

        self.labelUpdateTime.pack()
        self.labelcoingeckoApiGet.pack()
        self.labelcoingeckoApiCheck.pack(side = 'left')
        self.labelbinanceApiCheck.pack(side = 'left')

        self.btcPriceSec()
        self.apiCheckSec()
        self.currentPortfolio = CoinHoldingsTable(self.frameCoinHoldings)

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

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        self.arrHeadingTableLabel = []
        self.arrTableLabel = []
        self.arrTableData = []
        self.currentTableDisplayed = 'test.json'

        self.frameUserCoinHoldingsTable = tk.Frame(self.master, borderwidth = 2, relief = 'sunken')
        self.labelCurrentTableDisplayed = tk.Label(self.master, borderwidth = 2, relief = 'sunken')
        self.buttonUpdateTablePrices = tk.Button(self.master, borderwidth = 2)

        self.labelCurrentTableDisplayed.configure(text = self.currentTableDisplayed)
        self.buttonUpdateTablePrices.configure(text = 'Update Current Prices', command = (lambda : self.updateCoinHoldingTableCurrentPrices('coingecko')))

        self.createCoinHoldingsTableHeadings()
        self.createCoinHoldingsTable()
        self.updateCoinHoldingTableCurrentPrices('coingecko')

        self.labelCurrentTableDisplayed.grid(row = 0, column = 0)
        self.buttonUpdateTablePrices.grid(row = 0, column = 1)
        self.frameUserCoinHoldingsTable.grid(row = 1, column = 0, columnspan = 2)

    def createCoinHoldingsTableHeadings(self):

        try:
            with open('test.json','r') as jsonToOpen:
                userCoinHoldingsJSON = json.load(jsonToOpen)
        except json.JSONDecodeError:
            print('JSON file is empty, exiting function')
            return None

        try:
            coinHoldingsKeys = userCoinHoldingsJSON[0].keys()
            listCoinHoldingsKeys = list(coinHoldingsKeys)
            for key in range(len(listCoinHoldingsKeys)):
                self.headingTableLabel = tk.Label(self.frameUserCoinHoldingsTable, text = listCoinHoldingsKeys[key])
                self.headingTableLabel.grid(row = 0, column = key, padx = 1, pady = 1)
                self.arrHeadingTableLabel.append(listCoinHoldingsKeys[key])
        except IndexError:
            print('Error with file, no content')


    def createCoinHoldingsTable(self):

        rowInsert = 1
        columnInsert = 0
        try:
            with open('test.json','r') as jsonToOpen:
                userCoinHoldingsJSON = json.load(jsonToOpen)
        except json.JSONDecodeError:
            print('JSON file is empty, exiting function')
            return None

        for coinIndex in (userCoinHoldingsJSON):
            columnInsert = 0
            currentRowLabel = []
            currentRowData = {}
            currentRowKeys = userCoinHoldingsJSON[(rowInsert - 1)].keys()
            currentRowKeysList = list(currentRowKeys)
            for coinData in coinIndex.values():
                self.tableLabel = tk.Label(self.frameUserCoinHoldingsTable, text = coinData)
                self.tableLabel.grid(row = rowInsert, column = columnInsert, padx = 1, pady = 1)
                currentRowLabel.append(self.tableLabel)
                currentRowData.update({currentRowKeysList[columnInsert] : coinData})
                columnInsert += 1
            self.arrTableLabel.append(currentRowLabel)
            self.arrTableData.append(currentRowData)
            rowInsert += 1

    def saveCoinHoldingsTable(self):

        fileToWriteTo = 'test.json'
        if os.path.isfile(fileToWriteTo) == True:
            try:
                with open(fileToWriteTo, 'w') as jsonToWrite:
                    if self.arrTableData != []:
                        json.dump(self.arrTableData, jsonToWrite)
                    else:
                        print('arrTableData is empty')
            except json.JSONDecodeError:
                print('JSON file is empty, exiting function')
                return None

        else:
            try:
                with open(fileToWriteTo, 'w+') as jsonToWrite:
                    if self.arrTableData != []:
                        json.dump(self.arrTableData, jsonToWrite)
                    else:
                        print('arrTableData is empty')
            except json.JSONDecodeError:
                print('JSON file is empty, exiting function')
                return None

    def updateCoinHoldingTableEntry(self, coinToUpdate, fieldToUpdate, updatedData, toSave):

        cTU = coinToUpdate
        fTU = fieldToUpdate
        uD = updatedData

        for i in range(len(self.arrTableData)):
            if self.arrTableData[i]['name'] == cTU:
                self.arrTableData[i].update({fTU : uD})
                break

        for j in range(len(self.arrTableLabel[i])):
            if self.arrHeadingTableLabel[j] == fTU:
                labelToUpdate = self.arrTableLabel[i][j]
                labelToUpdate.configure(text = uD)
                break

        if toSave == True:
            self.saveCoinHoldingsTable()

    def updateCoinHoldingTableCurrentPrices(self, apiToUse):
        coinsToCheck = []
        for i in range(len(self.arrTableData)):
            coinsToCheck.append(self.arrTableData[i]['name'])
        coinsToSend = ','.join(coinsToCheck)
        if apiToUse == 'coingecko':
            uDJSON = api_service.coingeckoApiGet('/simple/price', 'JSON', {'ids':coinsToSend,'vs_currencies':'usd'})
            for i in range(len(self.arrTableData)):
                cTU = self.arrTableData[i]['name']
                uDDict = uDJSON.get(cTU)
                uD = uDDict['usd']
                self.updateCoinHoldingTableEntry(cTU, 'mostRecentPrice', uD, False)
                self.updateCoinHoldingTableEntry(cTU, 'mostRecentTime', datetime.now().strftime('%H:%M:%S'), False)

            self.saveCoinHoldingsTable()


def main():
    root = tk.Tk()
    MainApp(root)
    root.tk.mainloop()

if __name__ == '__main__':
    main()
