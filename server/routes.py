import logging
from main import app
from vertex import vertex_client
from vertex.utils import *
from server.decorators import token_required, params_validation


@app.route("/quote/product=<product_id>&amount=<amount>")
@params_validation
def quote(product_id, amount):
    """
    Get quote for amount
    :param product_id:
    :param amount:
    :return:
    """
    try:
        logging.info("Get quote for %s %s", amount, product_id)
        result = vertex_client.get_market_liquidity(product_id, 1000)
        return create_quote_response(amount, result)
    except Exception as e:
        logging.error('Quote error: %s', str(e))
        return {"error": True, "msg": str(e)}


@app.route("/execute/product=<product_id>&side=<side>&amount=<amount>&price=<price>")
@params_validation
@token_required
def execute(product_id, side, amount, price):
    """
    Execute order
    :param product_id:
    :param side:
    :param amount:
    :param price:
    :return:
    """
    try:
        logging.info("Execute %s %s %s %s", product_id, side, amount, price)
        response = vertex_client.execute(product_id, side, amount, price)
        return simulate_order_execution(response)
    except Exception as e:
        logging.error('Execute error: %s', str(e))
        return {"error": True, "msg": str(e)}


@app.route("/markets")
def markets():
    """
    Get all markets
    :return:
    """
    try:
        logging.info("Get all markets...")
        response = vertex_client.get_pairs()
        return create_markets_response(response)
    except Exception as e:
        logging.error('Markets error: %s', str(e))
        return {"error": True, "msg": str(e)}


@app.route("/ob/product_id=<product_id>&depth=<depth>", methods=['GET'])
@params_validation
def ob(product_id, depth):
    """
    Get orderbook
    :param product_id:
    :param depth:
    :return:
    """
    try:
        logging.info("Get orderbook for %s %s", product_id, depth)
        response = vertex_client.get_market_liquidity(product_id, depth)
        return create_orderbook_response(response)
    except Exception as e:
        logging.error('Orderbook error: %s', str(e))
        return {"error": True, "msg": str(e)}


@app.route("/")
@token_required
def home():
    """
    Get home page
    :return:
    """
    logging.info("Get home page...")
    return home_page_response()
