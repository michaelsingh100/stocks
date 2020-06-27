from ..models import Tickers
from ..models import ClosingPoints
from ..models import VolumePoints
import datetime
from pandas_datareader import data
import pandas as pd
from pandas_datareader._utils import RemoteDataError
import time
import threading
from pathlib import Path

class PullTickerData:
    default_start = datetime.datetime(2016, 1, 4)
    default_end = datetime.datetime.now()
    default_time_format = '%Y-%m-%d'
    default_source = 'yahoo'
    log_dir = "/home/ubuntu/logs"


    def start_pulling(self):
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)
        threads = []
        for c in range(65, 91):
            t = threading.Thread(target=self.pull_remaining_data, args=(char(c),))
            threads.append(t)
            t.start()

    def pull_remaining_data(self, letter):
        data_to_fetch = list()
        tickers = Tickers.objects.raw("select symbol from Tickers WHERE symbol REGEXP '^[%s]'" % (letter))

        for ticker in tickers:
            # last_date = ClosingPoints.objects.raw('select max(date) AS recent,max(id) AS id from ClosingPoints where symbol = "%s"' % (ticker))
            # if last_date and last_date[0].recent is not None:
            #     last_date = datetime.datetime.strptime(last_date[0].recent, "%Y-%m-%d")
            #     if last_date.date() < self.default_end.date():
            #         data_to_fetch.append((ticker.symbol,last_date + datetime.timedelta(days=1)))
            # else:
            data_to_fetch.append((ticker.symbol, PullTickerData.default_start))
        if len(data_to_fetch) > 0 :
            self.update_data_in_db(data_to_fetch,letter)

    def update_data_in_db(self, points, filename):
        # point[0] = ticker point[1] = start time
        with open(self.log_dir + "/" + letter + ".txt","a+") as fh:
            for point in points:
                ticker = point[0]
                start_date = point[1]
                fh.write("Pulling %s data" % (ticker))
                try:
                    report = data.DataReader([ticker],
                                start=start_date.strftime(self.default_time_format),
                                data_source=self.default_source)
                except RemoteDataError as exp:
                    print("%s doesn't exist. remote error" % (ticker))
                    continue
                closing = report['Adj Close']
                close_enteries = (ClosingPoints(symbol=ticker, date=row[0], price=row[1]) for row in closing[ticker].iteritems())
                ClosingPoints.objects.bulk_create(close_enteries, ignore_conflicts=True)
                fh.write("Added Close for %s" % (ticker))

                volume = report['Volume']
                vol_enteries = (VolumePoints(symbol=ticker, date=vol[0], volume=vol[1]) for vol in volume[ticker].iteritems())
                VolumePoints.objects.bulk_create(vol_enteries, ignore_conflicts=True)
                fh.write("Added Volume for %s" % (ticker))
                fh.write("sleeping for .2 seconds")
                time.sleep(.5)
