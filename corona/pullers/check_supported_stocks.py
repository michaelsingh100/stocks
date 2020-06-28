from ..models import Tickers
from ..utils import get_chunks
import threading
from pandas_datareader import data
import datetime
import math
from ..models import Tickers
import robin_stocks as r

class SupportChecker:
    def __init__(self):
        self.log_file = "/home/ubuntu/logs/suported.log"
    def update_support(self):
        for c in range(65, 91):
            tickers = Tickers.objects.raw("select symbol from Tickers WHERE symbol REGEXP '^[%s]'" % (chr(c)))
            tickers = (tick.symbol for tick in tickers)
            threads = []
            tickers = get_chunks(tickers,5)
            for i in range (0,5):
                t = threading.Thread(target=self.update_supported, args=(tickers.pop(),chr(c)))
                threads.append(t)
                t.start()

            for thrd in threads:
                thrd.join()

    def update_supported(self,lst):
        #Check yahoo reader support
        try:
            report = data.get_data_yahoo(lst,start=datetime.datetime.now() - datetime.timedelta(days=3))['Adj Close']
            for symbol in lst:
                if math.isnan(report['Adj Close'][symbol][0]):
                    t = Tickers.objects.get(symbol=symbol)
                    t.supported = False
                    t.save(['supported'])
                else:
                    t = Tickers.objects.get(symbol=symbol)
                    t.supported = True
                    t.save(['supported'])
        except:
            for symbol in lst:
                t = Tickers.objects.get(symbol=symbol)
                t.supported = False
                t.save(['supported'])

        #Check robhin hood support
        r.login("michaelsingh100@gmail.com","Hiall234@@")
        for symbol in lst:
            if r.get_stock_quote_by_symbol(symbol) is None:
                t = Tickers.objects.get(symbol=symbol)
                t.supported = False
                t.save(['supported'])
            else:
                t = Tickers.objects.get(symbol=symbol)
                t.supported = True
                t.save(['supported'])

