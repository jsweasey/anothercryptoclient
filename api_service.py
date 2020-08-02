import requests
import json
import time as time

binanceApiAddress = 'https://api.binance.com/api/v3'
binancePingEndpoint = '/ping'

coingeckoApiAddress = 'https://api.coingecko.com/api/v3'
coingeckoPingEndpoint = '/ping'

def binanceApiCheck():
    try:
        binanceCheckResponse = requests.get(binanceApiAddress + binancePingEndpoint)
        if binanceCheckResponse.status_code == 200:
            return True, 0
        else:
            return False, binanceCheckResponse.status_code
    except:
        return False, 0

def binanceApiGet(endpoint, returnType, *params):
    try:
        binanceApiGetAddress = (binanceApiAddress + endpoint)
        binanceGetResponse = requests.get(binanceApiGetAddress, *params)
        if returnType == 'RESPONSE':
            return binanceGetResponse
        elif returnType == 'JSON':
            return binanceGetResponse.json()
        elif returnType == 'TEXT':
            return binanceGetResponse.text
        else:
            return 'RETURN TYPE NOT DEFINED'

    except:
        return 'ERROR OCCURRED IN binanceApiGet()'

def coingeckoApiCheck():
    try:
        coingeckoCheckResponse = requests.get(coingeckoApiAddress + coingeckoPingEndpoint)
        if coingeckoCheckResponse.status_code == 200:
            return True, 0
        else:
            return False, coingeckoCheckResponse.status_code
    except:
        return False, 0

def coingeckoApiGet(endpoint, returnType, *params):
    try:
        coingeckoApiGetAddress = (coingeckoApiAddress + endpoint)
        coingeckoGetResponse = requests.get(coingeckoApiGetAddress, *params)
        if returnType == 'RESPONSE':
            return coingeckoGetResponse
        elif returnType == 'JSON':
            return coingeckoGetResponse.json()
        elif returnType == 'TEXT':
            return coingeckoGetResponse.text
        else:
            return 'RETURN TYPE NOT DEFINED'
    except:
        return 'ERROR OCCURRED IN coingeckoApiGet()'
