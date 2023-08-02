import threading;
import robin_stocks;
import robin_stocks.robinhood as r;
import pyotp;

lastPriceUsed = 0.00;
lastAction = "";
token = "";
email = "";
password = "";

def init():
    totp  = pyotp.TOTP(token).now();
    login = r.login(email, password, mfa_code=totp);

def setInterval(time):
    e = threading.Event()
    while not e.wait(time):
        getPrice("BTC")

def getPrice(symbol):
    price = robin_stocks.robinhood.crypto.get_crypto_quote(symbol);
    decimalPrice = price['bid_price'];
    quantity = round((3.00 / float(decimalPrice)), 8);
    print("price", round(float(decimalPrice), 2));

    positions = robin_stocks.robinhood.crypto.get_crypto_positions();
    availableAmount = positions[0]['quantity_available'];
    priceToSell = round((float(availableAmount) * float(decimalPrice)), 2);
    print("priceToSell", priceToSell);
    print("lastPriceUsed", lastPriceUsed);
    
    if lastAction == "" or lastAction == "sell":
        # buy
        buy(quantity, float(decimalPrice));

    if lastAction == "buy" and priceToSell > lastPriceUsed:
        # sell
        sell(float(priceToSell));

def buy(quantity, price):
    global lastAction;
    global lastPriceUsed;
    buyOrder = robin_stocks.robinhood.orders.order_buy_crypto_by_quantity("BTC", quantity, timeInForce='gtc', jsonify=True);
    boughtPrice = price;
    # lastPriceUsed = round(float(boughtPrice), 2) * quantity;
    lastPriceUsed = 3.01;
    print("Buy", buyOrder);
    lastAction = "buy";

def sell(price):
    global lastAction;
    sellOrder = robin_stocks.robinhood.orders.order_sell_crypto_by_price("BTC", price, timeInForce='gtc', jsonify=True);
    print("Sell", sellOrder);
    lastAction = "sell";

# using
init();
# setInterval(0.10)
setInterval(0.25)
# positions = robin_stocks.robinhood.crypto.get_crypto_positions();
# print("positions", positions);

