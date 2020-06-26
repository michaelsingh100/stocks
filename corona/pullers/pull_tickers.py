import datetime
import requests
from bs4 import BeautifulSoup
import re
from ..models import Tickers
from ..models import Earnings
import json


class PullTickers:

    def __init__(self):
        self.total = list()

    def by_vol_and_earn(self,start=datetime.datetime.now()-datetime.timedelta(days=5), end=datetime.datetime.now() + datetime.timedelta(days=5)):
        self.by_volume()
        self.by_earn(start, end)
        self.update_to_db()


    def by_volume(self):

        for i in range(0, 4):
            offset = i*100
            url = "https://finance.yahoo.com/most-active?offset="+str(offset)+"&amp;count=100"
            page = requests.get(url).text
            soup = BeautifulSoup(page, features="html.parser")

            for rows in soup.find_all('tr', attrs={'class' : re.compile('.*simpTblRow.*')}):
                stock = list()
                stock.append(rows.find('td', attrs={'aria-label':'Symbol'}).text)
                stock.append(rows.find('td', attrs={'aria-label':'Name'}).text)
                self.total.append(stock)

    def by_earn(self,start=datetime.datetime.now()-datetime.timedelta(days=5), end=datetime.datetime.now() + datetime.timedelta(days=5)):
        for_earnings = []
        earning_days = []
        for day_count in range((end-start).days + 1):
            day = start + datetime.timedelta(days=day_count)
            earning_days.append(day.strftime("%Y-%m-%d"))
        limit = 1
        offset = 0
        check = False
        for day in earning_days:
            limit = 1
            offset = 0
            while offset < limit:
                url = "https://finance.yahoo.com/calendar/earnings?day=" + day + "&amp;offset=" + str(offset*100) + "&amp;size=100"
                data = requests.get(url).text
                soup = BeautifulSoup(data,features="html.parser")
                s_rows = soup.find_all('tr', attrs={'class':re.compile('.*simpTblRow.*')})
                if len(s_rows) > 100 and not check:
                    limit = s_rows / 100
                    check = True
                for rows in s_rows:
                    symbol = rows.find('td', attrs={'aria-label':'Symbol'}).text
                    company = rows.find('td', attrs={'aria-label':'Company'}).text
                    call_time = rows.find('td', attrs={'aria-label':'Earnings Call Time'}).text
                    eps_est = rows.find('td', attrs={'aria-label':'EPS Estimate'}).text
                    reported_est = rows.find('td', attrs={'aria-label':'Reported EPS'}).text
                    surprise = rows.find('td', attrs={'aria-label':'Surprise(%)'}).text
                    stock = []
                    stock.append(symbol)
                    stock.append(company)
                    self.total.append(stock)
                    for_earnings.append((symbol,day,call_time,eps_est,reported_est,surprise))
                offset = offset + 1

        self.fetch_from_zac_and_update_earnings_to_db(for_earnings)

    def fetch_from_zac_and_update_earnings_to_db(self, tickers):
        conv = lambda i : i or None
        url = "https://quote-feed.zacks.com/index.php?t=%s"
        for tick in tickers:
            data = requests.get(url % (tick[0])).content
            j_data = json.loads(data)
            print(tick[0])
            if "error" not in j_data[tick[0]]:
                zac_rank = conv(j_data[tick[0]]["zacks_rank"])
                zac_rank_value = conv(j_data[tick[0]]["zacks_rank_text"])

                Earnings.objects.update_or_create(symbol = tick[0],
                                                  defaults={"zac_score":zac_rank,"zac_score_value":zac_rank_value,
                                                            "upcoming_date":tick[1], "upcoming_time":tick[2]},)
                print("Recorded Info for %s" % (tick[0]))


    def update_to_db(self):
        enteries = (Tickers(symbol=ticker[0],name=ticker[1]) for ticker in self.total)
        Tickers.objects.bulk_create(enteries,ignore_conflicts=True)
