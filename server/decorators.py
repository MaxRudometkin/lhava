from functools import wraps
from vertex import vertex_client


def token_required(f):
    """
    Decorate routes to require token in header
    :param f:
    :return:
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        # TODO: read token from header
        return f(*args, **kwargs)

    return wrap


def params_validation(f):
    """
    Decorate routes to validate params
    :param f:
    :return:
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if "product_id" in kwargs:
            symbol = vertex_client.get_symbol(kwargs["product_id"])
            if symbol is None:
                return {"error": True, "msg": "Invalid product_id"}

        if "side" in kwargs:
            if kwargs['side'] not in ['buy', 'sell']:
                return {"error": True, "msg": "Invalid 'side' value"}

        if "amount" in kwargs:
            try:
                float(kwargs["amount"])
            except:
                return {"error": True, "msg": "Invalid 'amount' value"}

        if "price" in kwargs:
            try:
                float(kwargs["price"])
            except:
                return {"error": True, "msg": "Invalid 'price' value"}

        return f(*args, **kwargs)

    return wrap
