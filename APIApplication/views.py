from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests
from datetime import datetime
from .models import *
import json

@api_view(["GET"])
def ListCoins(request):
    """
    Used the /coins/list endpoint on https://www.coingecko.com/en/api/v3 url to retrieve
    a list of coin ids, symbols and names
    """
    url = "https://api.coingecko.com/api/v3/coins/list"
    date_now = datetime.now().date()
    try:
        # First check if data was already pulled Today, if not request data for Today
        # and store it in the database.
        all_events = CoinList.objects.get(date=date_now).json_str
    except CoinList.DoesNotExist:
        CoinList.objects.all().delete()
        all_events = requests.get(url).text
        list_coin_obj = CoinList(date=date_now, json_str=all_events)
        list_coin_obj.save()
    event_JSON = json.loads(all_events)
    return JsonResponse(event_JSON, safe=False)
@api_view(["GET"])
def MarketCap(request):
    """
    Used the /market_chart endpoint on https://www.coingecko.com/en/api/v3 url to calculate and
    retrieve the market cap for the wanted coin id and currency pair for the given date.
    Made sure that I always get a given days market cap by passing 91 days as a parameter even if the
    date passed is not 91 days ago, if however it is more than 91 days ago I will pass the number of
    days in the past we would like data for.
    """
    coin_id = request.GET.get('coin_id','')
    currency = request.GET.get('currency', '')
    date_now = datetime.now().date()
    key = "error"
    dict_response = {}
    try:
        # First check if the date input is in the correct format, if not return error on exception
        date = datetime.strptime(request.GET.get('date', ''), '%Y/%m/%d')
        date_str = date.strftime('%d-%m-%Y')
        url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/history?date={date_str}'
        market_cap = f'Coin id ({coin_id}) and currency ({currency}) combination does not have a market cap value for {date_str} date as of yet.'
        try:
            # First check if today's date is in the the MCap DB, if not truncate the table.
            # Would like to rather make a crontab job for this so that it wont check everytime
            # a request is sent.
            date_check = list(MCap.objects.filter(date_captured=date_now))
            market_cap = MCap.objects.get(date_captured=date_now, input_date=date, coin_id=coin_id, currency=currency).market_cap
            key = currency
        except MCap.DoesNotExist:
            if len(date_check) == 0:
                MCap.objects.all().delete()
            try:
                # First check if response contains market cap detail.
                # Then check if market cap can be retrieved for given currency provided,
                # if not return a error message
                market_caps = requests.get(url).json()['market_data']['market_cap']
                market_cap = market_caps[currency]
                list_mcap_obj = MCap(date_captured=date_now, input_date=date, coin_id=coin_id, currency=currency,
                                     market_cap=market_cap)
                list_mcap_obj.save()
                key = currency
            except KeyError:
                dict_response[key] = market_cap
                return JsonResponse(dict_response, safe=False, status=404)
    except ValueError:
        return JsonResponse({'error':'Invalid date please use yyyy/mm/dd format'}, safe=False, status=400)
    dict_response[key] = market_cap
    return JsonResponse(dict_response, safe=False)

