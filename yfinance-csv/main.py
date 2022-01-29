from symtable import Symbol
import yfinance as yf

def yahooSymbolExportToCsv(symbol):
    doge = yf.Ticker(symbol)

    df = doge.history(period="max")
    df.index.names = ['date']
    df.columns = ['open', 'high', 'low', 'close', 'volume', 'dividend', 'split']
    df = df[['open', 'high', 'low', 'close', 'volume',  'split', 'dividend']] 
    df.to_csv(f"{symbol}.csv", sep="\t")

yahooSymbolExportToCsv("DOGE-USD")
