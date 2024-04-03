from vertex_protocol.utils.math import from_x18
from flask import url_for


def create_orderbook_response(order_book):
    """
    Creates an orderbook response.
    :param order_book:
    :return:
    """
    data = {
        "ts": order_book["response"].timestamp,
        "bids": [[from_x18(int(price)), from_x18(int(size))] for price, size in order_book["response"].bids],
        "asks": [[from_x18(int(price)), from_x18(int(size))] for price, size in order_book["response"].asks]
    }

    order_book.update(data)
    del order_book["response"]
    return order_book


def create_markets_response(markets):
    """
    Creates a markets response.
    :param markets:
    :return:
    """
    return [{"symbol": symbol, "product_id": product_id} for symbol, product_id in markets.items()]


def create_quote_response(amount, order_book):
    """
    Creates a quote response.
    :param amount:
    :param order_book:
    :return:
    """
    buy_price, buy_amount = calculate_avg_price(amount, order_book["response"].asks)
    sell_price, sell_amount = calculate_avg_price(amount, order_book["response"].bids)

    msg = "success"
    if buy_amount < float(amount) or sell_amount < float(amount):
        msg = "Not enough liquidity on a market. Try smaller order size."

    result = {"msg": msg, "ts": order_book["response"].timestamp,
              "buy_quote": {"price": buy_price, "amount": buy_amount},
              "sell_quote": {"price": sell_price, "amount": sell_amount}}
    order_book.update(result)
    del order_book["response"]
    del order_book["depth"]
    return order_book


def calculate_avg_price(amount, order_book):
    """
    Calculates the average price of the order book.
    :param amount:
    :param order_book:
    :return:
    """
    amount = float(amount)
    price = 0
    size = 0
    for ask in order_book:

        if size >= amount:
            break

        ob_price, ob_size = from_x18(int(ask[0])), from_x18(int(ask[1]))
        current_size = ob_size
        if ob_size >= amount - size:
            current_size = amount - size

        price = ((price * size) + (ob_price * current_size)) / (current_size + size)
        size += current_size

    return price, size


def home_page_response():
    """
    Creates the home page response.
    :return:
    """
    content = "Available endpoints:</br>"

    content += "</br></br></br>- /quote (params: product_id: int, amount: number)</br>"
    content += "Examples:</br>"
    content += f"<a href='{url_for('quote', product_id=3, amount=100)}'>/quote/product_id=3&amount=100</a> - get quote for 100 ETH</br>"
    content += f"<a href='{url_for('quote', product_id=2, amount=10)}'>/quote/product_id=40&amount=10</a> - get quote for 10 BTC</br>"

    content += "</br></br></br>- /execute (params: product_id:int, side: buy/sell:, amount: number:, price: number:)</br>"
    content += "Examples:</br>"
    content += f"<a href='{url_for('execute', product_id=3, amount=100, price=123, side='buy')}'>/execute/product=3&side=buy&amount=100&price=123</a> - buy 100 3 for price of 123</br>"
    content += f"<a href='{url_for('execute', product_id=2, amount=10, price=12, side='sell')}'>/execute/product=2&side=sell&amount=10&price=12</a> - wsell 10 2 for price of 12</br>"

    content += "</br></br></br>- /ob (params: product_id: int, depth: number)</br>"
    content += "Examples:</br>"
    content += f"<a href='{url_for('ob', product_id=3, depth=5)}'>/ob/product_id=3&depth=100</a> - get orderbook for 100 depth ETH</br>"
    content += f"<a href='{url_for('ob', product_id=2, depth=10)}'>/ob/product_id=2&depth=10</a> - get quote for 10 depth BTC</br>"

    content += "</br></br></br>- /markets</br>"
    content += "Examples:</br>"
    content += f"<a href='{url_for('markets')}'>/markets</a> - get all markets</br>"

    return content


def simulate_order_execution(response):
    """
    Simulates the order execution.
    :param response:
    :return:
    """
    if response["side"] == "buy":
        price, size = calculate_avg_price(response["amount"], response["response"].asks)
    else:
        price, size = calculate_avg_price(response["amount"], response["response"].bids)

    status = 'fully_filled' if size == float(response["amount"]) else 'partially_filled'
    result = {"price": price, "size": size, "status": status}
    response.update(result)
    del response["response"]
    del response["depth"]

    return response
