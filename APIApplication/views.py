from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests
from datetime import datetime
from .models import *
import json

@api_view(["GET"])
###########################################################################################################
### Used the /coins/list endpoint on https://www.coingecko.com/en/api/v3 url to retrieve                ###
### a list of coin ids, symbols and names                                                              ###
###########################################################################################################
def ListCoins(request):
    url = "https://api.coingecko.com/api/v3/coins/list"
    date_now = datetime.now().date()
    try:
        all_events = str(CoinList.objects.filter(Date=date_now)[0])
    except IndexError:
        print('Hello')
        CoinList.objects.all().delete()
        all_events = requests.get(url).text
        list_coin_obj = CoinList(Date=date_now, jason_str=all_events)
        list_coin_obj.save()
    event_JSON = json.loads(all_events)
    return JsonResponse(event_JSON, safe=False)
@api_view(["GET"])
###########################################################################################################
### Used the /market_chart endpoint on https://www.coingecko.com/en/api/v3 url to calculate and         ###
### retrieve the market cap for the wanted coin id and currency pair for the given date.                ###
### Made sure that I always get a given days market cap by passing 91 days as a parameter even if the   ###
### date passed is not 91 days ago, if however it is more than 91 days ago I will pass the number of    ###
### days in the past we would like data for.                                                            ###
###########################################################################################################
def MarketCap(request):
    coin_id = request.GET.get('coin_id','')
    try:
        date = datetime.strptime(request.GET.get('date', ''), '%Y/%m/%d').date()
        currency = request.GET.get('currency', '')
        date_now = datetime.now().date()
        date_diff = (date_now - date).days
        if date_diff <= 90:
            days = 91
        else:
            days = date_diff + 1
        url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency={currency}&days={days}'

        try:
            clear_all = True
            Date_check = str(MCap.objects.filter(Date_captured=date_now)[0])
            clear_all = False
            market_cap = float(
                MCap.objects.filter(Date_captured=date_now, Input_date=date, coin_id=coin_id, currency=currency)[0])
        except IndexError:
            if clear_all == True:
                MCap.objects.all().delete()
            try:
                market_caps = requests.get(url).json()['market_caps']
                for i in range(len(market_caps) - 1):
                    if date == datetime.fromtimestamp(market_caps[i][0] / 1000).date():
                        market_cap = market_caps[i][1]
                list_mcap_obj = MCap(Date_captured=date_now, Input_date=date, coin_id=coin_id, currency=currency,
                                     Market_cap=market_cap)
                list_mcap_obj.save()
            except KeyError:
                return JsonResponse(requests.get(url).json(), safe=False)
    except ValueError:
        return JsonResponse({'error':'Invalid date please use yyyy/mm/dd format'}, safe=False)

    dict_response = {}
    dict_response[currency] = market_cap
    return JsonResponse(dict_response, safe=False)

