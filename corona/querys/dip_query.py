from ..models import Tickers
from ..models import AvgVolume
from ..models import Earnings
from ..models import Growth
from ..models import ClosingPoints


class DipQueries:

    def get_table(self,start,end,limit):
        table_info = []
        table_info.append(["Symbol", "Company", "Total Avg", "Zac Score", "Zac Value","Total Growth"])
        tickers = AvgVolume.objects.raw("select symbol,total_avg from AvgVolume order by total_avg DESC LIMIT %s" % (limit))

        for tick in tickers:
            tick_info = []
            name_result = Tickers.objects.raw("select name,symbol from Tickers where symbol = '%s'" % tick.symbol)
            name = name_result[0].name
            tick_info.append(tick.symbol)
            tick_info.append(name)
            tick_info.append(tick.total_avg)
            earnings_result = Earnings.objects.raw("select zac_score, zac_score_value,symbol from Earnings where symbol = '%s'" % tick.symbol)
            if earnings_result:
                earnings = earnings_result[0]
                tick_info.append(earnings.zac_score)
                tick_info.append(earnings.zac_score_value)
            else:
                tick_info.append("")
                tick_info.append("")
            growth = Growth.objects.raw("select symbol, y_2020 from Growth where symbol = '%s'" % tick.symbol)
            if growth:
                tick_info.append(growth[0].y_2020)
            else:
                tick_info.append("")

            table_info.append(tick_info)

        return table_info

    def get_droppers(request,start,end, limit):


        table_with_start_end_price = "(select max(id) as id, symbol, MAX(IF(a.date >= '%s 00:00:00' AND a.date < '%s 23:00:00'," \
                " a.price, 0)) as start, MAX(IF(a.date >= '%s 00:00:00' AND a.date < '%s 23:00:00'," \
                " a.price, 0)) as end" % (start,start,end,end)
        table_with_details = "(select id,A.symbol as symbol,name, start, end, ROUND(((end - start)/start)*100,2) as Difference" \
                " from %s from ClosingPoints a GROUP BY symbol) as A,Tickers where A.symbol = Tickers.symbol and end IS NOT NULL and end > 0 order by Difference ) AS tab" \
                             % (table_with_start_end_price)
        table_with_details2 = "(select id,tab.symbol as symbol,name,start,end,Difference,day_avg_30 from %s ,AvgVolume " \
                                            "where AvgVolume.symbol = tab.symbol and Difference < 0 order by Difference LIMIT %s) AS cab" % (table_with_details,limit)

        results = ClosingPoints.objects.raw("select id,cab.symbol as symbol,name,start,end,Difference,day_avg_30,zac_score,zac_score_value " \
                                            "from %s left outer join Earnings on Earnings.symbol = cab.symbol" % (table_with_details2))
        
        return results



#
