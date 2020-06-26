from django.shortcuts import render
from django.http import HttpResponse
# from .models import Tinkers
# from .models import ClosingPoints
# from .models import ClosedData
# from datetime import datetime

import datetime
from pandas_datareader import data
import pandas as pd
import yfinance
import matplotlib.pyplot as plt
from .querys.dip_query import DipQueries
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

plt.switch_backend('Agg')

BASE = "/Users/Michael/django_stock/stocks/corona/static/corona/images/stock_reports"


def index(request):
    if request.method == 'POST':
        #entered form, could be volume or earnings
        start = request.POST['start']
        end = request.POST['end']
        limit = request.POST['limit']
        dipper = DipQueries()
        biggest_dips = dipper.get_droppers(start,end,limit)
        headers = ["id","symbol","name","start","end","Difference","day_avg_30","Zac Score", "Zac Value"]
        reports = biggest_dips
        return render(request, 'corona/index.html', {'reports': reports, 'headers':headers})
    else:
        context = {"date" :datetime.datetime.now().strftime('%Y-%m-%d')}
        return render(request, 'corona/index.html', context)

#
# def update_report_pngs(request):
#     if request.method == 'GET':
#         params = request.GET
#         if 'start' not in params or 'end' not in params:
#             return HttpResponse(status=404)
#         try:
#             print(params['start'])
#             start = datetime.strptime(params['start'], '%Y-%m-%d')
#             end = datetime.strptime(params['end'], '%Y-%m-%d')
#             delta = end - start
#         except ValueError:
#             return HttpResponse("Invalid Date", status=400)
#
#         symbols = Tinkers.objects.values_list('symbol', flat=True)
#
#         reports = data.DataReader(symbols,
#                         start=params['start'],
#                         end=params['end'],
#                         data_source='yahoo')['Adj Close']
#
#         for symbol in symbols:
#             pth = BASE + "/" + symbol + "/" + params['start']
#             if not os.path.exists(pth):
#                 os.makedirs(pth)
#             txt_path = pth + "/" + str(delta.days) + ".png"
#             if not os.path.exists(txt_path):
#                 ds = reports[symbol]
#                 plt.figure()
#                 plt.plot(ds)
#                 plt.title("Tinker: %s Start: %s Range(days): %d" % (symbol, params['start'], delta.days))
#                 plt.savefig(txt_path)
#                 plt.close('all')
#
#         return HttpResponse(status=200)
#     else:
#         return HttpResponse("Not allowed")
#
#
# def get_droppers(request):
#     if request.method == 'GET':
#         params = request.GET
#         if 'start' not in params or 'end' not in params or 'limit' not in params:
#             return HttpResponse(status=404)
#
#         try:
#             start = datetime.strptime(params['start'], '%Y-%m-%d')
#             end = datetime.strptime(params['end'], '%Y-%m-%d')
#             limit = int(params['limit'])
#             delta = end - start
#         except ValueError:
#             return HttpResponse("Invalid Date", status=400)
#
#         results = ClosedData.objects.raw("select id,A.symbol,name, start, end, ROUND(((end - start)/start)*100,2) as Difference" \
#                 " from (select max(id) as id, symbol, MAX(IF(a.date >= '%s 00:00:00' AND a.date < '%s 23:00:00'," \
#                 " a.price, 0)) as start, MAX(IF(a.date >= '%s 00:00:00' AND a.date < '%s 23:00:00'," \
#                 " a.price, 0)) AS end from corona_closeddata a GROUP BY symbol) as A,corona_tinkers where A.symbol = corona_tinkers.symbol order by Difference LIMIT %d" %
#                                          (params['start'],params['start'],params['end'],params['end'], limit))
#
#         paginator = Paginator(results, 9)
#         page = request.GET.get('page', 1)
#         try:
#             reports = paginator.page(page)
#         except PageNotAnInteger:
#             reports = paginator.page(1)
#         except EmptyPage:
#             reports = paginator.page(paginator.num_pages)
#
#         return render(request, 'corona/index1.html', {'reports': reports, 'delta': delta.days , 'start': params['start'], 'end': params['end']})
#     else:
#         return HttpResponse("Not allowed")
#
