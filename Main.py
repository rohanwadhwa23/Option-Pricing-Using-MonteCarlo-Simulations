import Ticker_Data
import Webpage
import Graph
    
if __name__ == "__main__":
    
    stock = Ticker_Data.Ticker_Data()
    
    webpage = Webpage.Webpage()
    webpage.layout(stock.get_ticker_list(), stock.get_ticker_data())
    webpage.server_run(8060)
