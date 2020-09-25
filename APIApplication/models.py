from django.db import models

class CoinList(models.Model):
    Date = models.DateTimeField()
    jason_str = models.TextField(max_length=34783)

    def __str__(self):
        return self.jason_str

class MCap(models.Model):
    Date_captured = models.DateTimeField()
    coin_id = models.CharField(max_length=50)
    Input_date = models.DateTimeField()
    currency = models.CharField(max_length=50)
    Market_cap = models.FloatField()

    def __float__(self):
        return self.Market_cap
