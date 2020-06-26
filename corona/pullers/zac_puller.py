from ..models import Tickers
from ..models import Earnings
import requests
import json

class ZacPuller:
    def __init__(self):
        print("Starting to pull from zac")

    def fetch_from_zac_and_update_earnings_to_db(self):
        ticks = Tickers.objects.raw("select symbol from Tickers");
        conv = lambda i : i or None
        url = "https://quote-feed.zacks.com/index.php?t=%s"
        for tick in ticks:
            try:
                data = requests.get(url % (tick.symbol)).content
                j_data = json.loads(data)
                print(tick.symbol)
                if "error" not in j_data[tick.symbol]:
                    zac_rank = conv(j_data[tick.symbol]["zacks_rank"])
                    zac_rank_value = conv(j_data[tick.symbol]["zacks_rank_text"])

                    Earnings.objects.update_or_create(symbol = tick.symbol,
                                                      defaults={"zac_score":zac_rank,"zac_score_value":zac_rank_value,})
                    print("Recorded Info for %s" % (tick.symbol))
            except:
                print("Failed on %s",tick.symbol)
