# Imports

# Data management
from pandas import Series, DataFrame
import pandas as pd

# Data collection
import pandas_datareader.data as web

# Data manipulation and visualization
from datetime import datetime

class Backtrader:
    """
    Backtrader - Evaluates trading strategies for stock performance
    """

    def __init__(self, stock, days=365):
        """
        Constructor
        stock - Stock ticker symbol
        days - Amount of previous days to test (default 365)
        """
        self.data = self.getData(stock)
        self.days = days
    
    def getData(self, ticker):
        """
        Finds data for given stock
        ticker - Stock symbol
        """
        df = web.DataReader(ticker, 'yahoo')
        return df
    
    def evaluate(self, strategy, ownership):
        """
        Evaluates a trading strategy and finds it's return ratio
        Strategy - Function (returns DataFrame) that appends new information to dataframe to evaluate ownership dates
        Ownership - Function (returns mask) that provides information on when to own a stock
        """
        # Run setup for ownership strategy and find ownership dates
        self.data = strategy(self.data)
        self.data['Own'] = ownership(self.data)
        
        # Find daily return rate and strategy daily return rate
        self.data['DRR'] = self.data['Close'] / self.data['Close'].shift(1)
        self.data['SDRR'] = self.data['DRR'][self.data['Own']].fillna(method='ffill')
        
        # Find product of buy + hold return rate and strategy return rate
        bhrr = self.data[len(self.data) - self.days:]['DRR'].prod()
        srr = self.data[len(self.data) - self.days:]['SDRR'].prod()
        
        # Print findings
        print("Buy and Hold Return Ratio:", bhrr)
        print("Strategy Return Ratio:", srr)
        print()
        
        if bhrr >= 1:
            print("This stock performed well over this time period.")
        else:
            print("This stock did not perform well over this time period.")
        
        if srr >= 1:
            if srr > bhrr:
                print("Your strategy performed exceptionally well.")
            else:
                print("Your strategy performed well, but you would be better off buying and holding.")
        else:
            if srr > bhrr:
                print("Your strategy performed better than buying and holding, but still did not perform well.")
            else:
                print("Your strategy did not perform well.")
    
    
    def plot(self, labels=["Close"]):
        """
        Plots important data specified by strategy
        Labels - dataframe columns to plot
        """
        return self.data[len(self.data) - self.days:][labels].plot()
        
    def plotOwnership(self):
        """
        Plots simple graph showing when to own stock
        """
        try:
            return self.data[len(self.data) - self.days:]['Own'].plot(ylim=[0, 2])
        except:
            print("You must evaluate your model before checking your returns.")

    def plotReturns(self):
        """
        Plots returns of strategy vs. simple buy and hold
        """
        try:
            return self.data[len(self.data) - self.days:][['DRR', 'SDRR']].cumprod().plot()
        except:
            print("You must evaluate your model before checking your returns.")