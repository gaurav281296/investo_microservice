from django.db import models
from django.db.models import CharField
from django.db.models import IntegerField
from django.db.models import BooleanField
from django.db.models import DecimalField


class Trade(models.Model):
    trade_id = models.AutoField(primary_key=True)
    portfolio_id = models.IntegerField(null=False, blank=False)
    ticker_name = models.CharField(max_length=10, blank=False, null=False)
    trade_type = models.CharField(max_length=1)
    trade_price = models.DecimalField(max_digits=10, decimal_places=2)
    trade_quantity = models.IntegerField(null=False, blank=False)

    class Meta:
        ordering = ['trade_id']


class Portfolio(models.Model):
    portfolio_id = models.IntegerField(db_index=True, null=False, blank=False)
    ticker_name = models.CharField(db_index=True, max_length=10, blank=False, null=False)
    avg_buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(null=False, blank=False)

    class Meta:
        ordering = ['portfolio_id']