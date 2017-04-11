class Strategy:
    """
    Base strategy class
    Specifies what each strategy must implement
    """
    def __init__(self):
        self.plotLabels = NotImplementedError("Must define plotLabels in constructor")
    
    def strategy(self, dataframe):
        raise NotImplementedError("Must implement `strategy()` method\nstrategy() evaluates dataframe and provides ownership data")
    
    def ownership(self, dataframe):
        raise NotImplementedError("Must implement `ownership()` method\nownership() returns a mask determining when to own a stock")