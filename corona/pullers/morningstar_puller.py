import requests
import json
from ..models import Tickers
from ..models import Growth
from bs4 import BeautifulSoup
import time
import re

class MorningStarPuller:
    exchs = ["XNYS","XNAS","ARCX","XASE","XNGS"]
    def __init__(self):
        print("Starting to pull from Morning star - Growth Info")
        self.tickers = Tickers.objects.raw("select symbol from Tickers")
    def pull_growth(self):
        url = "http://performance.morningstar.com/perform/Performance/stock/performance-history-1.action?"\
              "&t=%s:%s&region=usa&culture=en-US&cur=&ops=clear&s=0P00001MK8"\
              "ndec=2&ep=true&align=m&y=5&type=growth"
        for tick in self.tickers:
            grth_data = list()
            for exch in MorningStarPuller.exchs:
                page = requests.get(url % (exch,tick.symbol)).text
                if page is not "":
                    break

            if page is "":
                continue
            grth_data.append(tick.symbol)
            soup = BeautifulSoup(page, features="html.parser")
            chrt_div = soup.find("div", id="chart_container")
            grths = chrt_div.find('table').find('tbody').find('tr').find_all('td')
            for grth in grths:
                if grth.text is not "":
                    grth_data.append(float(grth.text))
                else:
                    grth_data.append(0.0)

            
            Growth.objects.update_or_create(symbol = grth_data[0], defaults={"y_2015":grth_data[1],"y_2016":grth_data[2], \
                               "y_2017":grth_data[3],"y_2018":grth_data[4],"y_2019":grth_data[5], \
                               "y_2020":grth_data[6]})
            print("Added %s growth info" % (tick.symbol))



