import json as json
import requests as requests
import api_service as api_service
import data_service as data_service
import tkinter as tk
from tkinter import messagebox
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
        currentPortfolio = CoinHoldingsTable(self.frameCoinHoldings)

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

        self.coinHasBeenChecked = False #FOR ADDING NEW COIN VALIDATION, REMOVE WHEN UPDATE VALIDATION METHOD
        self.checkedName = '' #FOR ADDING NEW COIN VALIDATION, REMOVE WHEN UPDATE VALIDATION METHOD
        self.checkedTicker = '' #FOR ADDING NEW COIN VALIDATION, REMOVE WHEN UPDATE VALIDATION METHOD

        self.frameUserCoinHoldingsTable = tk.Frame(self.master, borderwidth = 2, relief = 'sunken')
        self.labelCurrentTableDisplayed = tk.Label(self.master, borderwidth = 2, relief = 'sunken')
        self.buttonUpdateTablePrices = tk.Button(self.master, borderwidth = 2)
        self.buttonAddTestCoin = tk.Button(self.master, borderwidth = 2)

        self.labelCurrentTableDisplayed.configure(text = self.currentTableDisplayed)
        self.buttonUpdateTablePrices.configure(text = 'Update Current Prices', command = lambda: (self.updateCoinHoldingTableCurrentPrices()))
        self.buttonAddTestCoin.configure(text = 'Add New Coin', command = lambda: (self.addNewCoinForm()))

        self.createCoinHoldingsTable()
        self.updateCoinHoldingTableCurrentPrices()

        self.labelCurrentTableDisplayed.grid(row = 0, column = 0)

        self.buttonUpdateTablePrices.grid(row = 0, column = 1)
        self.buttonAddTestCoin.grid(row = 0, column = 2)

        self.frameUserCoinHoldingsTable.grid(row = 1, column = 0, columnspan = 2)

    def createCoinHoldingsTableHeadings(self):
        coinHoldingsKeys = Coin.currentCoinFields(False)
        listCoinHoldingsKeys = list(coinHoldingsKeys)
        for key in range(len(listCoinHoldingsKeys)):
            headingStr = re.sub(r"(?<=\w)([A-Z])", r" \1", listCoinHoldingsKeys[key]).title()
            self.headingTableLabel = tk.Label(self.frameUserCoinHoldingsTable, text = headingStr)
            self.headingTableLabel.grid(row = 0, column = key, padx = 1, pady = 1)
            self.arrHeadingTableLabel.append(listCoinHoldingsKeys[key])


    def createCoinHoldingsTable(self):

        self.createCoinHoldingsTableHeadings()

        rowInsert = 1
        columnInsert = 0
        self.arrTableLabel = []
        self.arrTableData = []

        for keyIndex in Coin.coinDict:
            columnInsert = 0
            currentRowLabel = []
            currentRowData = {}
            currentCoinDict = Coin.coinDict[keyIndex].dataDict(False)
            currentRowKeysList = Coin.currentCoinFields(False)
            for coinData in currentCoinDict.values():
                self.tableLabel = tk.Label(self.frameUserCoinHoldingsTable, text = coinData)
                self.tableLabel.grid(row = rowInsert, column = columnInsert, padx = 1, pady = 1)
                currentRowLabel.append(self.tableLabel)
                currentRowData.update({currentRowKeysList[columnInsert] : coinData})
                columnInsert += 1
            self.arrTableLabel.append(currentRowLabel)
            self.arrTableData.append(currentRowData)
            rowInsert += 1

    #def saveCoinHoldingsTable(self):
    #
    #    fileToWriteTo = (globalConfig[0].get('workingPortfolioFile'))
    #    print(self.arrTableData)
    #    data_service.saveToJSONFile(fileToWriteTo, self.arrTableData)

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
            Coin.saveCoins()

    def updateCoinHoldingTableCurrentPrices(self):
        print('updating price')
        Coin.updateCoinPrices('coingecko')
        for key in Coin.coinDict.keys():
            if Coin.coinDict[key].inExchange == 'True':
                self.updateCoinHoldingTableEntry(Coin.coinDict[key].name, 'mostRecentPrice', Coin.coinDict[key].mostRecentPrice, False)
                self.updateCoinHoldingTableEntry(Coin.coinDict[key].name, 'mostRecentTime', Coin.coinDict[key].mostRecentTime, False)

        Coin.saveCoins()

    def addNewCoinForm(self): #REPLACE WITH tkinter validate
        def addNewCoin():
            updatedDataDict = {}
            name = entryNCWName.get()
            ticker = entryNCWTicker.get()
            amount = entryNCWAmount.get()
            currency = omCurrency.get()
            price = entryNCWPrice.get()
            time = entryNCWTime.get()

            varDict = {'name':name,'ticker':ticker,'amount':amount,'currency':currency,'price':price,'time':time}

            fieldTypeIncorrect = False
            emptyFields = False

            for varData in list(varDict.keys()):
                if varDict[varData] == '':
                    emptyFields = True
                if varData == 'amount' or varData == 'price':
                    try:
                        int(varDict[varData])
                    except:
                        fieldTypeIncorrect = True

            coinAlreadyExist = False
            for keyToCheck in Coin.coinDict.keys():
                if keyToCheck == name:
                    coinAlreadyExist = True
                if Coin.coinDict[keyToCheck].ticker == ticker:
                    coinAlreadyExist = True

            try:
                if name != self.checkedName:
                    self.coinHasBeenChecked = False
            except:
                self.coinHasBeenChecked = False

            try:
                if ticker != self.checkedTicker:
                    self.coinHasBeenChecked = False
            except:
                self.coinHasBeenChecked = False

            if (coinAlreadyExist == False) and (emptyFields == False) and (fieldTypeIncorrect == False):
                if self.coinHasBeenChecked == True:
                    Coin.addCoin(entryNCWName.get())
                    updatedDataDict.clear()
                    updatedDataDict.update({'ticker':ticker,'amount':amount,'currencyBoughtIn':currency,'boughtAtPrice':price,'boughtAtTime':time,'inExchange':'True'})
                    Coin.coinDict[name].updateFields(updatedDataDict)
                    self.createCoinHoldingsTable()
                    Coin.saveCoins()
                    labelNCVInfo.configure(text = 'Coin: ' + name + ' added succesfully!')
                    self.coinHasBeenChecked = False
                else:
                    if messagebox.askyesno("Warning","Coin: " + name + " has not been checked against Coingecko database, proceed?"):
                        newCoinWindow.lift()
                        Coin.addCoin(entryNCWName.get())
                        updatedDataDict.clear()
                        updatedDataDict.update({'ticker':ticker,'amount':amount,'currencyBoughtIn':currency,'boughtAtPrice':price,'boughtAtTime':time})
                        Coin.coinDict[name].updateFields(updatedDataDict)
                        self.createCoinHoldingsTable()
                        Coin.saveCoins()
                        labelNCVInfo.configure(text = 'Coin: ' + name + ' added succesfully!')
                        self.coinHasBeenChecked = False
                    else:
                        newCoinWindow.lift()
            elif emptyFields == True:
                labelNCVInfo.configure(text = 'Not all Coin data fields have been filled!')
            elif coinAlreadyExist == True:
                labelNCVInfo.configure(text = 'Coin: ' + name + ' already exists!')
            elif fieldTypeIncorrect == True:
                labelNCVInfo.configure(text = 'One or more fields have incorrect data types!')
            else:
                labelNCVInfo.configure(text = 'Unknown error, please check all fields!')

        def checkCoinExists():
            name = entryNCWName.get()
            apiResponse = api_service.coingeckoApiGet('/coins/' + name, 'JSON', {'id':name,'localization':False,'tickers':False,'market_data':False,'community_data':False,'developer_data':False})
            if apiResponse.get('id') == name:
                labelNCVInfo.configure(text = 'Coin: ' + name + ' exists on Coingecko, added ticker!')
                entryNCWTicker.delete(0,tk.END)
                entryNCWTicker.insert(0,apiResponse.get('symbol'))
                self.checkedName = name
                self.checkedTicker = apiResponse.get('symbol')
                self.coinHasBeenChecked = True
            else:
                labelNCVInfo.configure(text = 'Coin: ' + name + ' does not exist on Coingecko!')
                self.coinHasBeenChecked = False

        newCoinWindow = tk.Toplevel()
        omCurrency = tk.StringVar(self)

        labelNCWName = tk.Label(newCoinWindow, text = 'Name')
        labelNCWTicker = tk.Label(newCoinWindow, text = 'Ticker')
        labelNCWAmount = tk.Label(newCoinWindow, text = 'Amount')
        labelNCWCurrency = tk.Label(newCoinWindow, text = 'Currency')
        labelNCWPrice = tk.Label(newCoinWindow, text = 'Price')
        labelNCWTime = tk.Label(newCoinWindow, text = 'Time')
        labelNCVInfo = tk.Label(newCoinWindow, text = '')

        entryNCWName = tk.Entry(newCoinWindow)
        entryNCWTicker = tk.Entry(newCoinWindow)
        entryNCWAmount = tk.Entry(newCoinWindow)
        entryNCWPrice = tk.Entry(newCoinWindow)
        entryNCWTime = tk.Entry(newCoinWindow)

        optionmenuNCWCurrnency = tk.OptionMenu(newCoinWindow, omCurrency, 'usd')

        labelNCWName.grid(row = 0, column = 0)
        labelNCWTicker.grid(row = 1, column = 0)
        labelNCWAmount.grid(row = 2, column = 0)
        labelNCWCurrency.grid(row = 3, column = 0)
        labelNCWPrice.grid(row = 4, column = 0)
        labelNCWTime.grid(row = 5, column = 0)
        labelNCVInfo.grid(row = 6, column = 0)

        entryNCWName.grid(row = 0, column = 1)
        entryNCWTicker.grid(row = 1, column = 1)
        entryNCWAmount.grid(row = 2, column = 1)
        optionmenuNCWCurrnency.grid(row = 3, column = 1)
        entryNCWPrice.grid(row = 4, column = 1)
        entryNCWTime.grid(row = 5, column = 1)

        buttonNCWSendData = tk.Button(newCoinWindow, text='Add Coin', command = lambda: addNewCoin()).grid(row = 6, column = 1)
        buttonNCWCheckCoin = tk.Button(newCoinWindow, text='Check Coin', command = lambda: checkCoinExists()).grid(row = 0, column = 2)



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
    def currentCoinFields(cls, returnNonDataFields):
        fieldsToRetun = list(vars(Coin.coinDict[(list(Coin.coinDict.keys())[0])]))
        if returnNonDataFields == True:
            return fieldsToRetun
        else:
            try:
                fieldsToRetun.remove('isDeleted')
                fieldsToRetun.remove('inExchange')
            except:
                pass
            return fieldsToRetun

    @classmethod
    def saveCoins(cls):
        dataToSave = []
        for coinToSave in Coin.listCoinClasses():
            dataToSave.append(Coin.coinDict[coinToSave].dataDict(True))
        data_service.saveToJSONFile(globalConfig[0].get('workingPortfolioFile'), dataToSave)

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
                self.inExchange = portfolioJSONData[currentCoinIndex]['inExchange']
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
            self.inExchange = "False"

        self.isDeleted = False

    def dataDict(self, returnNonDataFields):
        returnDict = vars(self).copy()
        if returnNonDataFields == True:
            return returnDict
        else:
            try:
                returnDict.pop('isDeleted')
                returnDict.pop('inExchange')
            except:
                pass
            return returnDict

    def updateFields(self, updatedDataDict):
        self.ticker = updatedDataDict.get('ticker')
        self.amount = updatedDataDict.get('amount')
        self.boughtAtPrice = updatedDataDict.get('boughtAtPrice')
        self.boughtAtTime = updatedDataDict.get('boughtAtTime')
        self.currencyBoughtIn = updatedDataDict.get('currencyBoughtIn')
        self.inExchange = updatedDataDict.get('inExchange')

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
    MainAppInstance = MainApp(root)
    MainApp(root)
    root.tk.mainloop()

if __name__ == '__main__':
    main()
