from ..models import Tickers
from ..utils.utils import get_chunks
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
            tickers = [str(tick.symbol) for tick in tickers]
            threads = []
            tickers = get_chunks(tickers,5)
            for i in range (0,5):
                t = threading.Thread(target=self.update_supported, args=([tickers.pop()]))
                threads.append(t)
                t.start()

            for thrd in threads:
                thrd.join()

    def update_supported(self,lst):
        #Check yahoo reader support
        for symbol in lst:
            try:
                report = data.get_data_yahoo(symbol,start=datetime.datetime.now() - datetime.timedelta(days=3))['Adj Close']
            except:
                Tickers.objects.update_or_create(symbol=symbol,defaults={"supported" : False})
                continue

            #Check robhin hood support
            if r.get_stock_quote_by_symbol(symbol) is None:
                Tickers.objects.update_or_create(symbol=symbol,defaults={"supported" : False})
                print("Successfully rejected unsupported %s" % symbol)
            else:
                Tickers.objects.update_or_create(symbol=symbol,defaults={"supported" : True})
                print("Successfuly added supported %s" % symbol)

