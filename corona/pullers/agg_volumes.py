from ..models import VolumePoints
from ..models import AvgVolume
from ..models import Tickers
import datetime

class AggVolume:
    default_time_format = '%Y-%m-%d'

    def __init__(self):
        print("Start volume aggregations from volume points table")

    def aggregate(self):
        tickers = Tickers.objects.raw("select symbol from Tickers")
        now = datetime.datetime.now()
        before_30 = now - datetime.timedelta(days=30)
        before_60 = now - datetime.timedelta(days=60)
        before_150 = now - datetime.timedelta(days=150)

        tick_enteries = (AvgVolume(symbol=tick.symbol) for tick in tickers)
        AvgVolume.objects.bulk_create(tick_enteries, ignore_conflicts=True)

        results = VolumePoints.objects.raw("select AVG(volume) AS avg, max(id) as id, symbol from VolumePoints " \
                                           "where date between '%s' and '%s' group by symbol" \
                                           % (before_30.strftime(self.default_time_format), now.strftime(self.default_time_format)))

        enteries = (AvgVolume(symbol=result.symbol,day_avg_30=result.avg) for result in results)

        AvgVolume.objects.bulk_update(enteries,['day_avg_30'])
        print("Updated 30 day Avg")

        results = VolumePoints.objects.raw("select AVG(volume) AS avg, max(id) as id, symbol from VolumePoints " \
                                   "where date between '%s' and '%s' group by symbol" \
                                   % (before_60.strftime(self.default_time_format), now.strftime(self.default_time_format)))

        enteries = (AvgVolume(symbol=result.symbol,day_avg_60=result.avg) for result in results)

        AvgVolume.objects.bulk_update(enteries,['day_avg_60'])
        print("Updated 60 day Avg")

        results = VolumePoints.objects.raw("select AVG(volume) AS avg, max(id) as id, symbol from VolumePoints " \
                                   "where date between '%s' and '%s' group by symbol" \
                                   % (before_150.strftime(self.default_time_format), now.strftime(self.default_time_format)))

        enteries = (AvgVolume(symbol=result.symbol,day_avg_150=result.avg) for result in results)

        AvgVolume.objects.bulk_update(enteries,['day_avg_150'])
        print("Updated 150 day Avg")

        results = VolumePoints.objects.raw("select AVG(volume) AS avg, max(id) as id, symbol from VolumePoints group by symbol");

        enteries = (AvgVolume(symbol=result.symbol,total_avg=result.avg) for result in results)

        AvgVolume.objects.bulk_update(enteries,['total_avg'])
        print("Updated total day Avg")


