from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests
from httplib2 import Http
from datetime import datetime

@api_view(["GET"])
###########################################################################################################
### Used the /coins/list endpoint on https://www.coingecko.com/en/api/v3 url to retrieve                ###
### a list of coin ids, symboles and names                                                              ###
###########################################################################################################
def ListCoins(request):
    h = Http()
    url = "https://api.coingecko.com/api/v3/coins/list"
    r = requests.get(url)
    return JsonResponse(r.json() ,safe=False)
@api_view(["GET"])
###########################################################################################################
### Used the /market_chart endpoint on https://www.coingecko.com/en/api/v3 url to claculate and         ###
### retrieve the market cap for the wanted coin id and currency pair for the given date.                ###
### Made sure that I always get a given days market cap by passing 91 days as a parameter even if the   ###
### date passed is not 91 days ago, if however it is more than 91 days ago I will pass the number of    ###
### days in the past we would like data for.                                                            ###
###########################################################################################################
def MarketCap(request):
    h = Http()
    coin_id = request.GET.get('coin_id','')
    date = datetime.strptime(request.GET.get('date', ''), '%Y/%m/%d').date()
    currancy = request.GET.get('currency', '')
    date_now = datetime.now().date()
    date_diff = (date_now - date).days
    if date_diff <= 90:
        days = 91
    else:
        days = date_diff + 1
    url =f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency={currancy}&days={days}'
    r = requests.get(url).json()['market_caps']
    dict_response = {}
    for i in range(len(r)-1):
        if date == datetime.fromtimestamp(r[i][0]/1000).date():
            dict_response[currancy] = r[i][1]
    return JsonResponse(dict_response, safe=False)