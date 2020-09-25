from django.db import models

class CoinList(models.Model):
    date = models.DateTimeField()
    json_str = models.TextField(max_length=34783)

class MCap(models.Model):
    date_captured = models.DateTimeField()
    coin_id = models.CharField(max_length=50)
    input_date = models.DateTimeField()
    currency = models.CharField(max_length=50)
    market_cap = models.FloatField()
