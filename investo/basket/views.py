from django.shortcuts import render

# Create your views here.

import json
import traceback
from basket.models import Trade, Portfolio
from basket.serializers import TradeSerializer, PortfolioSerializer, IndividualPortfolioSerializer
from basket.helpers import validate_trade, validate_deletion, execute_trade, update_portfolio, calculate_returns, recompute_portfolio
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status, generics
from django.forms.models import model_to_dict


class TradeList(generics.GenericAPIView):
    """
    List all trades, or create a new trade.
    """
    serializer_class = TradeSerializer
    def get(self, request, format=None):
        trades = Trade.objects.all()
        serializer = TradeSerializer(trades, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        trade_obj = json.loads(json.dumps(request.data))
        try:
            validate_trade(trade_obj)
            trade_obj = execute_trade(trade_obj)
            update_portfolio(trade_obj) #make this async
        except Exception as e:
            print(traceback.format_exc())
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(model_to_dict(trade_obj), status=status.HTTP_201_CREATED)
 
class TradeDetail(generics.GenericAPIView):
    """
    Retrieve, update or delete a code trade.
    """
    def get_object(self, pk):
        try:
            return Trade.objects.get(trade_id=pk)
        except Trade.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        trade = self.get_object(pk)
        serializer = TradeSerializer(trade)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        trade = self.get_object(pk)
        try:
            validate_deletion(trade)
            trade.delete()
            recompute_portfolio(trade.portfolio_id, trade.ticker_name)
        except Exception as e:
            print(traceback.format_exc())
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PortfolioList(generics.GenericAPIView):
    """
    List all portfolios
    """
    def get(self, request, format=None):
        portfolio = Portfolio.objects.all()
        serializer = PortfolioSerializer(portfolio, many=True)
        return Response(serializer.data)

class PortfolioDetail(generics.GenericAPIView):
    """
    Retrieve a portfolio
    """
    def get_object(self, pk):
        try:
            return Portfolio.objects.filter(portfolio_id=pk)
        except Portfolio.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        portfolio = self.get_object(pk)
        serializer = IndividualPortfolioSerializer(portfolio, many=True)
        return Response(serializer.data)

class Returns(generics.GenericAPIView):
    """
    Get portfolio returns
    """
    def get_object(self, pk):
        try:
            return Portfolio.objects.filter(portfolio_id=pk)
        except Portfolio.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        portfolio = self.get_object(pk)
        returns = calculate_returns(portfolio)
        return Response(returns)