from StockTicker.DataFetcher import getAllStockData
from StockTicker.Ticker import TickerTape


data = getAllStockData()
app = TickerTape(data)
app.mainloop()

