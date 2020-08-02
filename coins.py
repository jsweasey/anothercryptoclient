
class Coin(object):

    def __init__(self, name, ticker, currentSell, currentBuy, 24hrVolume):

        self.name = name
        self.ticker = ticker
        self.currentSell = currentSell
        self.currentBuy = currentBuy
        self.24hrVolume = 24hrVolume


class BTC(Coin):

    def __init__(self, name, ticker, currentSell, currentBuy, 24hrVolume):

        super().__init__(name, ticker, currentSell, currentBuy, 24hrVolume)

class ETH(Coin):

    def __init__(self, name, ticker, currentSell, currentBuy, 24hrVolume):

        super().__init__(name, ticker, currentSell, currentBuy, 24hrVolume)

class LTC(Coin):

    def __init__(self, name, ticker, currentSell, currentBuy, 24hrVolume):

        super().__init__(name, ticker, currentSell, currentBuy, 24hrVolume)
