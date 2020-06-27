from ..models import Tickers
from ..models import ClosingPoints
from ..models import VolumePoints
import datetime
from pandas_datareader import data
import pandas as pd
from pandas_datareader._utils import RemoteDataError
import time

class PullTickerData:
    default_start = datetime.datetime(2016, 1, 4)
    default_end = datetime.datetime.now()
    default_time_format = '%Y-%m-%d'
    default_source = 'yahoo'

    def pull_remaining_data(self):
        data_to_fetch = list()
        tickers = Tickers.objects.raw("select symbol from Tickers")

        for ticker in tickers:
            # last_date = ClosingPoints.objects.raw('select max(date) AS recent,max(id) AS id from ClosingPoints where symbol = "%s"' % (ticker))
            # if last_date and last_date[0].recent is not None:
            #     last_date = datetime.datetime.strptime(last_date[0].recent, "%Y-%m-%d")
            #     if last_date.date() < self.default_end.date():
            #         data_to_fetch.append((ticker.symbol,last_date + datetime.timedelta(days=1)))
            # else:
            data_to_fetch.append((ticker.symbol, PullTickerData.default_start))

        self.update_data_in_db(data_to_fetch)

    def update_data_in_db(self, points):
        # point[0] = ticker point[1] = start time
        for point in points:
            ticker = point[0]
            start_date = point[1]
            print("Pulling %s data" % (ticker))
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
            print("Added Close for %s" % (ticker))

            volume = report['Volume']
            vol_enteries = (VolumePoints(symbol=ticker, date=vol[0], volume=vol[1]) for vol in volume[ticker].iteritems())
            VolumePoints.objects.bulk_create(vol_enteries, ignore_conflicts=True)
            print("Added Volume for %s" % (ticker))
            print("sleeping for .2 seconds")
            time.sleep(.2)
