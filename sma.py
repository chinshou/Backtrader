from strategy import Strategy
import pandas as pd
from pandas import DataFrame, Series

class SMACrossover(Strategy):
    """
    SMA Crossover Strategy
    Trades based on rolling average crossover of stock prices
    """
    def __init__(self, shortDays=30, longDays=180):
        """
        Constructor
        shortDays - Initial rolling average to evaluate
        longDays - Rolling average to compare shortDays to
        """    
        self.shortDays = shortDays
        self.longDays = longDays
        
        self.shortSMA = str(shortDays) + '-Day SMA'
        self.longSMA = str(longDays) + '-Day SMA'
        
        self.plotLabels = ['Close', self.shortSMA, self.longSMA]
    
    def strategy(self, dataframe):
        """
        Adds shortDay-SMA and longDay-SMA to given dataframe
        dataframe - Date-based dataframe loaded from Backtrader
        """
        dataframe[self.shortSMA] = dataframe['Close'].rolling(window=self.shortDays, min_periods=10).mean()
        dataframe[self.longSMA] = dataframe['Close'].rolling(window=self.longDays, min_periods=10).mean()
        return dataframe
    
    def ownership(self, dataframe):
        """
        Creates an ownership mask using information from self.strategy()
        dataframe - Date-based dataframe loaded from Backtrader
        """
        return (dataframe[self.shortSMA] > dataframe[self.longSMA]).shift(1).fillna(False)