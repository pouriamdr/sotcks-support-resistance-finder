import numpy as np
import requests, time, traceback, gc
from io import StringIO
import matplotlib.pyplot as plt
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

class TREND:
    def __init__(self):
        self.market = None
        self.limit = None
        self.type = None
        self.urls = {
            "market": "https://api.coinex.com/perpetual/v1/market/deals",
            "klines": "https://api.coinex.com/perpetual/v1/market/kline"
        }
        self.exit_program = False
        self.klines = None
    def get_market_klines(self):
        klines = {}
        while True:
            if self.exit_program == True:
                break
            try:
                req = requests.get(self.urls['klines'], params={"market":self.market, "limit": self.limit, "type": self.type}, headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"}, timeout=4).json()
                klines = req['data']
                if 'data' in req:
                    break
            except:
                traceback.print_exc()
            time.sleep(0.5)
        del req
        return klines
    def get_market_price(self):
        price = 0.0
        while True:
            if self.exit_program == True:
                break
            try:
                req = requests.get(self.urls['market'], params={"market":self.market, "limit": 1}, headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"}, timeout=4).json()
                if 'data' in req:
                    price = float(req['data'][0]['price'])
                    break
            except:
                traceback.print_exc()
            time.sleep(0.2)
        del req
        return price
    def isSupport(self, df,i):
        support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
        return support
    def isResistance(self, df,i):
        resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
        return resistance
    def isFarFromLevel(self, l, levels):
        return np.sum([abs(l-x) < self.s  for x in levels]) == 0
    def handler(self, market, type, limit, takeFar):
        self.market = market.upper()
        self.limit = int(limit)
        self.type = type
        takeFar = takeFar.upper()
        try:
            self.klines = self.get_market_klines()
            klines = 'Time,Open,Close,High,Low,Amount,Value,date_id\n'
            i = 0
            for kline in self.klines:
                kline[0] = str(kline[0])
                klines += ','.join(kline) + ',{}\n'.format(i) 
                i += 1
            df = pd.read_csv(StringIO(klines))
            df['high_trend'] = df['Close'].min()
            df['low_trend'] = df['Close'].min()
            self.s = np.mean(df['High'] - df['Low'])
            # START defining
            price = df['Close'][self.limit-1]
            resistance = price * 1000 
            support = 0
            levels = []
            # END.
            for i in range(2,df.shape[0]-2): # Identify all supports and resistances
                if self.isSupport(df,i):
                    l = df['Low'][i]
                    if takeFar == 'Y':
                        levels.append((i,l))
                    else:
                        if self.isFarFromLevel(l, levels):
                            levels.append((i,l))
                elif self.isResistance(df,i):
                    l = df['High'][i]
                    if takeFar == 'Y':
                        levels.append((i,l))
                    else:
                        if self.isFarFromLevel(l, levels):
                            levels.append((i,l))
            
            for level in levels: # Identify nearest support and resistance
                if level[1] > price and level[1] < resistance:
                    resistance = level[1]
                if level[1] < price and level[1] > support:
                    support = level[1]
            next_resistance = price * 1000
            prev_support = 0
            for level in levels: # Identify previus support and resistance
                if level[1] > price and level[1] < next_resistance and level[1] != resistance:
                    next_resistance = level[1]
                if level[1] < price and level[1] > prev_support and level[1] != support:
                    prev_support = level[1]
            
            print("Current: {}\nNext resistance: {}\nPrevious support: {}".format(self.get_market_price(), next_resistance, prev_support))

            fig = plt.figure()
            width = .5
            width2 = .05

            up = df[df.Close>=df.Open]
            down = df[df.Close<df.Open]

            # Define colors to use
            col1 = 'green'
            col2 = 'red'

            # Plot up prices
            plt.bar(up.index,up.Close-up.Open,width,bottom=up.Open,color=col1)
            plt.bar(up.index,up.High-up.Close,width2,bottom=up.Close,color=col1)
            plt.bar(up.index,up.Low-up.Open,width2,bottom=up.Open,color=col1)

            # Plot down prices
            plt.bar(down.index,down.Close-down.Open,width,bottom=down.Open,color=col2)
            plt.bar(down.index,down.High-down.Open,width2,bottom=down.Open,color=col2)
            plt.bar(down.index,down.Low-down.Close,width2,bottom=down.Close,color=col2)

            rows = df.shape[0] - 2
            # Rotate x-axis tick labels
            plt.xticks(rotation=45, ha='right')
            d = 's&r\n'
            for level in levels:
                d = d + str(level[1]) + '\n'
                plt.hlines(level[1],level[0], rows,colors='blue')
            plt.legend()
            plt.savefig('results/{}-{}-{}.pdf'.format(self.market, self.type, self.limit), dpi=fig.dpi)
            f = open('results/{}-{}-{}.csv'.format(self.market, self.type, self.limit), 'w')
            f.write(d)
            f.close()
            plt.show()
        except:
            traceback.print_exc()
        gc.collect()
    def close_threads(self):
        try:
            gc.collect()
            self.exit_program = True
        except:
            self.exit_program = True
            traceback.print_exc()
trend = TREND()
trend.handler('btcusdt', '1hour', 1000, 'n')