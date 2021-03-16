from rest_framework import serializers
from basket.models import Trade
from basket.models import Portfolio

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['trade_id', 'portfolio_id', 'ticker_name', 'trade_type', 'trade_price', 'trade_quantity']

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['portfolio_id', 'ticker_name', 'avg_buy_price', 'quantity']

class IndividualPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['ticker_name', 'avg_buy_price', 'quantity']