from ..models import ClosingPoints
from ..models import Statistics

class MeanPuller:
    def updatemean(self,start):
        results = ClosingPoints.objects.raw("select symbol, avg(price) as mean, std(price) as stan where date > '%s 00:00:00' group by symbol" % (start))

        enhan = (Statistics(symbol=result.symbol,mean_2020=result.mean,std_2020=result.stan) for result in results)

        Statistics.bulk_create(enhan, ignore_conflicts=True)
