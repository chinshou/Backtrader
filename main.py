from backtrader import Backtrader
from sma import SMACrossover

def main():
    # Instantiate trader
    trader = Backtrader('TSLA', 365)

    # Instantiate SMA crossover strategy
    # 30, 180 vs 10, 20
    crossover = SMACrossover(10, 20)

    # Evaluate model using strategy
    trader.evaluate(crossover.strategy, crossover.ownership)

if __name__ == '__main__':
    main()