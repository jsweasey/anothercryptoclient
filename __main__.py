import json as json
import requests as requests
import api_service as api_service
import data_service as data_service
import tkinter as tk
import time as time
import os as os
import re as re
from datetime import datetime as datetime

global globalConfig
global configPortfolioFile

with open('config.json', 'r') as jsonConfigFile:
    globalConfig = json.load(jsonConfigFile)

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
        self.currentTableDisplayed = globalConfig[0].get('workingPortfolioFile')

        self.frameUserCoinHoldingsTable = tk.Frame(self.master, borderwidth = 2, relief = 'sunken')
        self.labelCurrentTableDisplayed = tk.Label(self.master, borderwidth = 2, relief = 'sunken')
        self.buttonUpdateTablePrices = tk.Button(self.master, borderwidth = 2)

        self.labelCurrentTableDisplayed.configure(text = self.currentTableDisplayed)
        self.buttonUpdateTablePrices.configure(text = 'Update Current Prices', command = lambda: (self.updateCoinHoldingTableCurrentPrices()))

        self.createCoinHoldingsTableHeadings()
        self.createCoinHoldingsTable()
        self.updateCoinHoldingTableCurrentPrices()

        self.labelCurrentTableDisplayed.grid(row = 0, column = 0)
        self.buttonUpdateTablePrices.grid(row = 0, column = 1)
        self.frameUserCoinHoldingsTable.grid(row = 1, column = 0, columnspan = 2)

    def createCoinHoldingsTableHeadings(self):
        coinHoldingsKeys = Coin.currentCoinFields()
        listCoinHoldingsKeys = list(coinHoldingsKeys)
        for key in range(len(listCoinHoldingsKeys)):
            headingStr = re.sub(r"(?<=\w)([A-Z])", r" \1", listCoinHoldingsKeys[key]).title()
            self.headingTableLabel = tk.Label(self.frameUserCoinHoldingsTable, text = headingStr)
            self.headingTableLabel.grid(row = 0, column = key, padx = 1, pady = 1)
            self.arrHeadingTableLabel.append(listCoinHoldingsKeys[key])


    def createCoinHoldingsTable(self):

        rowInsert = 1
        columnInsert = 0

        for keyIndex in Coin.coinDict:
            columnInsert = 0
            currentRowLabel = []
            currentRowData = {}
            currentCoinDict = Coin.coinDict[keyIndex].dataDict()
            currentRowKeysList = list(currentCoinDict.keys())
            for coinData in currentCoinDict.values():
                self.tableLabel = tk.Label(self.frameUserCoinHoldingsTable, text = coinData)
                self.tableLabel.grid(row = rowInsert, column = columnInsert, padx = 1, pady = 1)
                currentRowLabel.append(self.tableLabel)
                currentRowData.update({currentRowKeysList[columnInsert] : coinData})
                columnInsert += 1
            self.arrTableLabel.append(currentRowLabel)
            self.arrTableData.append(currentRowData)
            rowInsert += 1

    def saveCoinHoldingsTable(self):

        fileToWriteTo = (globalConfig[0].get('workingPortfolioFile'))
        data_service.saveToJSONFile(fileToWriteTo, self.arrTableData)

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

    def updateCoinHoldingTableCurrentPrices(self):
        print('updating price')
        Coin.updateCoinPrices('coingecko')
        keyList = list(Coin.coinDict.keys())
        for keyIndex in range(Coin.totalCoins()):
            key = keyList[keyIndex]
            self.updateCoinHoldingTableEntry(Coin.coinDict[key].name, 'mostRecentPrice', Coin.coinDict[key].mostRecentPrice, False)
            self.updateCoinHoldingTableEntry(Coin.coinDict[key].name, 'mostRecentTime', Coin.coinDict[key].mostRecentTime, False)

        self.saveCoinHoldingsTable()


class Coin():

    coinDict = {}

    @classmethod
    def totalCoins(cls):
        return len(Coin.coinDict)

    @classmethod
    def listCoinClasses(cls):
        return Coin.coinDict

    @classmethod
    def initializeCoins(cls, fileLocation):
        coinsDataJSON = data_service.readJSONFile(fileLocation)
        for i in range(len(coinsDataJSON)):
            Coin.coinDict.update({(coinsDataJSON[i]['name']):(Coin(coinsDataJSON[i]['name']))})

    @classmethod
    def addCoin(cls, coinName):
        if Coin.coinDict.get(coinName, False) == False:
            Coin.coinDict.update({(coinName):(Coin(coinName))})

    @classmethod
    def updateCoinPrices(cls, apiToUse):
        coinsToCheckList = []
        for key in Coin.coinDict.keys():
            coinsToCheckList.append(key)
        coinsToCheckStr = ','.join(coinsToCheckList)
        updatePriceJSON = api_service.coingeckoApiGet('/simple/price', 'JSON', {'ids':coinsToCheckStr,'vs_currencies':'usd'})
        for key in Coin.coinDict.keys():
            Coin.coinDict[key].mostRecentPrice = updatePriceJSON.get(key).get('usd')
            Coin.coinDict[key].mostRecentTime = datetime.now().strftime('%H:%M:%S')

    @classmethod
    def currentCoinFields(cls): #ADD FIELD CHOOSING FUNCTIONALITY (E.G REMOVE ONLY isDeleted OR OTHER ATTRIBUTES)
        fieldsToRetun = list(Coin.coinDict[(list(Coin.coinDict.keys())[0])].__dict__)
        print(fieldsToRetun)
        try:
            fieldsToRetun.remove('isDeleted')
        except:
            pass
        return fieldsToRetun

    #@classmethod
    #def coinData(cls):


    def __init__(self, name):
        self.name = name
        coinFoundInJSON = False
        portfolioJSONData = data_service.readJSONFile(globalConfig[0].get('workingPortfolioFile'))
        for currentCoinIndex in range(len(portfolioJSONData)):
            if portfolioJSONData[currentCoinIndex]['name'] == self.name:
                self.ticker = portfolioJSONData[currentCoinIndex]['ticker']
                self.amount = portfolioJSONData[currentCoinIndex]['amount']
                self.boughtAtPrice = portfolioJSONData[currentCoinIndex]['boughtAtPrice']
                self.boughtAtTime = portfolioJSONData[currentCoinIndex]['boughtAtTime']
                self.currencyBoughtIn = portfolioJSONData[currentCoinIndex]['currencyBoughtIn']
                self.mostRecentPrice = portfolioJSONData[currentCoinIndex]['mostRecentPrice']
                self.mostRecentTime = portfolioJSONData[currentCoinIndex]['mostRecentTime']
                coinFoundInJSON = True
                break

        if coinFoundInJSON == False:
            self.ticker = '-'
            self.amount = '0'
            self.boughtAtPrice = '0'
            self.boughtAtTime = '-'
            self.currencyBoughtIn = '-'
            self.mostRecentPrice = '0'
            self.mostRecentTime = '-'

        self.isDeleted = False

    def dataDict(self):
        returnDict = self.__dict__
        try:
            returnDict.pop('isDeleted')
        except:
            pass
        return returnDict

    def changeInPriceAbsolute(self):
        priceChange = (self.currentPrice - self.boughtAtPrice)
        return priceChange

    def changeInPricePercentage(self, returnType):
        priceChange = (self.currentPrice - self.boughtAtPrice)
        percentageChange = (((priceChange/currentPrice)*100)-100)
        percentageChangeStr = percentageChange.str() + '%'
        if returnType == 'str':
            return percentageChangeStr
        elif returnType == 'int':
            return percentageChange
        else:
            return 'Invalid returnType'

    def delSelf(self):
        Coin.coinDict.pop(self.name)
        self.isDeleted = True




    #use this as main storage in program itself
    #use sqlite for database
    #make class methods for storage and organization of each Coin instance



def main():
    Coin.initializeCoins(globalConfig[0].get('workingPortfolioFile'))
    root = tk.Tk()
    MainApp(root)
    root.tk.mainloop()

if __name__ == '__main__':
    main()
