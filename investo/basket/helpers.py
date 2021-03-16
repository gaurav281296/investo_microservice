import decimal
from basket.models import Trade, Portfolio

def validate_trade(trade_data):
    trade_data["ticker_name"] = trade_data["ticker_name"].casefold()
    trade_data["trade_quantity"] = int(trade_data["trade_quantity"])
    trade_data["trade_price"] = decimal.Decimal(trade_data["trade_price"])
    trade_data["trade_type"] = trade_data["trade_type"].casefold()
    if trade_data["trade_price"] < 0.01:
        raise Exception("trade_price cannot be negative or zero")
    if trade_data["trade_type"].casefold() not in ["b", "s"]:
        raise Exception("trade_type can only be 'S' or 'B'")
    if trade_data["trade_quantity"] < 1:
        raise Exception("trade_quantity has to be more than 0")
    if trade_data["trade_type"].casefold() == "b":
        trade_data["success"] = True
    else:
        try:
            portfolio = Portfolio.objects.get(portfolio_id=trade_data["portfolio_id"],ticker_name=trade_data["ticker_name"])
        except Portfolio.DoesNotExist:
            raise Exception("sold quantity more than holding - short selling is not supported")

        if portfolio.quantity < trade_data["trade_quantity"]:
            raise Exception("sold quantity more than holding - short selling is not supported")           

def validate_deletion(trade_data):
    if trade_data.trade_type == "b":
        portfolio = Portfolio.objects.get(portfolio_id=trade_data.portfolio_id,ticker_name=trade_data.ticker_name)
        if portfolio.quantity < trade_data.trade_quantity:
            raise Exception("sold quantity will become more than bought quantity in portfolio - trade deletion not possible")

def recompute_portfolio(portfolio_id, ticker_name):
    portfolio = Portfolio.objects.get(portfolio_id=portfolio_id,ticker_name=ticker_name)
    trades = Trade.objects.filter(portfolio_id=portfolio_id,ticker_name=ticker_name)
    avg_buy_price = 0
    quantity = 0
    #will be in order of trade_id
    for trade in trades:
        if trade.trade_type == "b":
            avg_buy_price = ((avg_buy_price*quantity)+(trade.trade_price*trade.trade_quantity))/(quantity+trade.trade_quantity)
            quantity+=trade.trade_quantity
        else:
            quantity-=trade.trade_quantity
    portfolio.avg_buy_price = avg_buy_price
    portfolio.quantity = quantity
    if quantity == 0:
        portfolio.delete()
    else:
        portfolio.save()

def execute_trade(trade_data):
    trade = Trade(portfolio_id=trade_data["portfolio_id"],
        ticker_name=trade_data["ticker_name"],
        trade_type=trade_data["trade_type"].casefold(),
        trade_price=trade_data["trade_price"],
        trade_quantity=trade_data["trade_quantity"])
    trade.save()
    return trade

def update_portfolio(trade_data):
    try:
        portfolio = Portfolio.objects.get(portfolio_id=trade_data.portfolio_id,ticker_name=trade_data.ticker_name)
        if trade_data.trade_type == "b":
            new_quantity = portfolio.quantity + trade_data.trade_quantity
            new_avg_buy = ((portfolio.avg_buy_price*portfolio.quantity) + (trade_data.trade_quantity*trade_data.trade_price))/new_quantity
            portfolio.quantity = new_quantity
            portfolio.avg_buy_price = new_avg_buy
        else:
            portfolio.quantity -= trade_data.trade_quantity
        if portfolio.quantity > 0:
            portfolio.save()
        else:
            portfolio.delete()
    except Portfolio.DoesNotExist:
        portfolio = Portfolio(portfolio_id=trade_data.portfolio_id,
            ticker_name=trade_data.ticker_name,
            avg_buy_price=trade_data.trade_price,
            quantity=trade_data.trade_quantity)
        portfolio.save()

def calculate_returns(portfolio):
    cumulative_returns = 0
    for ticker in portfolio:
        cumulative_returns+=((100 - ticker.avg_buy_price)*(ticker.quantity))
    return cumulative_returns