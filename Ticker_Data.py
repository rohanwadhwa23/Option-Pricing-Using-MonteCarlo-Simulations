import numpy as np
import pandas as pd
import yfinance as yf

class Ticker_Data:

    def __init__(self):
        self.ticker_list = pd.read_csv("Data/Tickers.csv")
        #self.ticker_list = pd.read_csv("Data/Tickers_Full.csv")
        self.ticker_data = yf.download(self.ticker_list.Ticker.to_list(),'2020-1-1','2022-12-31', auto_adjust=True)#['Close']
            
    def get_ticker_list(self):
        return self.ticker_list
    
    def get_ticker_data(self):
        return self.ticker_data