from django.core.management.base import BaseCommand
from ...pullers.pull_data import PullTickerData
from ...pullers.pull_tickers import PullTickers
from ...pullers.agg_volumes import AggVolume
from ...pullers.morningstar_puller import MorningStarPuller
from ...pullers.zac_puller import ZacPuller
from ...pullers.one_time_ticker_parser import  TickerUpdater
import datetime
import time
from ...pullers.agg_mean import MeanPuller
from ...pullers.check_supported_stocks import SupportChecker

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        a = datetime.datetime.now()
        #Check new supports
        support = SupportChecker()
        support.update_support()
        # #get tickers by highest volume on day, and earnings =/- 5 days
        #ticker_updater = PullTickers()
        #ticker_updater.by_vol_and_earn()

        #Update tickers
        # ticker_updater = TickerUpdater()
        # ticker_updater.parse_tickers()
        #
        # #Pull data from last finding to current day for all tickers in db
        # data_updater = PullTickerData()
        # #data_updater.start_pulling()
        # data_updater.fix_data()

        #Agregate the volumes
        #aggregator = AggVolume()
        #aggregator.aggregate()
        #
        # #Adds in growth info from morningstar
        # puller = MorningStarPuller()
        # puller.pull_growth()
        #
        # #Pull from zac score
        # zac_puller = ZacPuller()
        # zac_puller.fetch_from_zac_and_update_earnings_to_db()

        #Agg mean and std
        # mean_puller = MeanPuller()
        # mean_puller.updatemean("2020-01-06")
        print(datetime.datetime.now() - a) 
