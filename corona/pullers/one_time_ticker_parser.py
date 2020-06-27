import json
from ..models import Tickers
class TickerUpdater:
    # nasq_file = "/home/ubuntu/django_stock/stocks/corona/static/corona/nasdaq_json.json"
    # nysq_file = "/home/ubuntu/django_stock/stocks/corona/static/corona/nyse-listed_json.json"
    nysq_file = "/home/ubuntu/django_stock/stocks/corona/static/corona/nyse-rest.json"

    def parse_tickers(self):
        # nasq = []
        # with open(self.nasq_file) as file:
        #     nasq_js = json.load(file)
        #     for stock in nasq_js["stocks"]:
        #         nasq.append(Tickers(symbol=stock['ACT Symbol'],name=stock['Company Name']))
        # Tickers.objects.bulk_create(nasq,ignore_conflicts=True)
        #
        # nyse = []
        # with open(self.nysq_file) as file:
        #     nysq_js = json.load(file)
        #     for stock in nysq_js["stocks"]:
        #         nyse.append(Tickers(symbol=stock['ACT Symbol'],name=stock['Company Name']))
        # Tickers.objects.bulk_create(nyse,ignore_conflicts=True)


        nyse = []
        with open(self.nysq_file) as file:
            nysq_js = json.load(file)
            for stock in nysq_js["stocks"]:
                nyse.append(Tickers(symbol=stock['Symbol'],name=stock['Security Name']))
        Tickers.objects.bulk_create(nyse,ignore_conflicts=True)

