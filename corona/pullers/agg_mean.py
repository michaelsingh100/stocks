from ..models import ClosingPoints
from ..models import Statistics

class MeanPuller:
    def updatemean(self,start):
        results = ClosingPoints.objects.raw("select max(id) as id, symbol, avg(price) as mean, std(price) as stan from ClosingPoints where date > '%s 00:00:00' group by symbol" % (start))

        enhan = (Statistics(symbol=result.symbol,mean_2020=result.mean,std_2020=result.stan) for result in results)

        Statistics.objects.bulk_create(enhan, ignore_conflicts=True)

    def updateZ(self,limit):
        results = ClosingPoints.objects.raw("select id,symbol,((nt.price - Statistics.mean_2020)/Statistics.std_2020) as z_score from (select id, symbol, price from (select max(date) as id ,symbol from ClosingPoints group by symbol) as " \
                                            "dates left join ClosingPoints on dates.symbol = ClosingPoints.symbol and dates.id = ClosingPoints.date) as nt," \
                                            "Statistics where nt.symbol = Statistics.symbol order by z_score ASC LIMIT %s" % (limit))

        r
