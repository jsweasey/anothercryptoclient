import json
import os as os

def saveToJSONFile(fileToSave, dataToSave):
    fileCheck = fileToSave.split('.')
    try:
        if fileCheck[1] == 'json':
            fileToSaveExt = fileToSave
        else:
            fileToSaveExt = fileToSave + '.json'
    except IndexError:
        fileToSaveExt = fileToSave + '.json'

    if os.path.isfile(fileToSaveExt) == True:
        try:
            with open(fileToSaveExt, 'w') as jsonToWrite:
                if dataToSave != []:
                    json.dump(dataToSave, jsonToWrite)
                else:
                    print('Data to save is empty')
        except:
            print('Error with saving')
    else:
        createNewJSONFile(fileToSave)
        saveToJSONFile(fileToSave, dataToSave)


def createNewJSONFile(fileToCreate):
    fileCheck = fileToCreate.split('.')
    try:
        if fileCheck[1] == 'json':
            fileToCreateExt = fileToCreate
        else:
            fileToCreateExt = fileToCreate + '.json'
    except IndexError:
        fileToCreateExt = fileToCreate + '.json'

    if os.path.isfile(fileToCreateExt) == False:
        try:
            with open(fileToCreateExt, 'w+') as jsonToWrite:
                json.dump([], jsonToWrite)
        except:
            print('Error with creating')

    else:
        print('File: ' + fileToCreateExt + ', already exists, suggest using saveToJSONFile or addToJSONFile')

def addToJSONFile(fileToSave, dataToSave):
    fileCheck = fileToSave.split('.')
    try:
        if fileCheck[1] == 'json':
            fileToSaveExt = fileToSave
        else:
            fileToSaveExt = fileToSave + '.json'
    except IndexError:
        fileToSaveExt = fileToSave + '.json'

    if os.path.isfile(fileToSaveExt) == True:
        try:
            if dataToSave != []:
                with open(fileToSaveExt, 'r') as jsonToOpen:
                    dataToAddTo = json.load(jsonToOpen)
                dataToSave.update(dataToAddTo)
                with open(fileToSaveExt, 'w') as jsonToWrite:
                    json.dump(dataToSave, jsonToWrite)
            else:
                print('Data to save is empty')
        except:
            print('Error with saving')
    else:
        print('File: ' + fileToSaveExt + ', does not exist yet, suggest using createNewJSONFile')


def readJSONFile(fileToRead):
    fileCheck = fileToRead.split('.')
    try:
        if fileCheck[1] == 'json':
            fileToReadExt = fileToRead
        else:
            fileToReadExt = fileToRead + '.json'
    except IndexError:
        fileToReadExt = fileToRead + '.json'

    if os.path.isfile(fileToReadExt) == True:
        try:
            with open(fileToReadExt, 'r') as jsonToOpen:
                readJSONData = json.load(jsonToOpen)
                return readJSONData
        except:
            print('Error with reading')
    else:
        print('File: ' + fileToReadExt + ', does not exist yet, suggest using createNewJSONFile')

def removeFromJSONFile(fileToEdit,):
    pass
