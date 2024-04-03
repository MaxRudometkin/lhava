from vertex_protocol.client import create_vertex_client
import logging

class VertexClient:
    def __init__(self, client_mode, private_key):
        """
        Create client for interacting with the Vertex Protocol
        :param client_mode:
        :param private_key:
        """
        self.client = create_vertex_client(client_mode, private_key)
        self.pairs = self.get_pairs()

    def get_pairs(self):
        """
        Get all pairs
        :return:
        """
        logging.info('requesting all pairs...')
        symbols = self.client.market.get_all_product_symbols()
        return {str(s.product_id): s.symbol for s in symbols}

    def get_symbol(self, product_id):
        """
        Get symbol for product
        :param product_id:
        :return:
        """
        logging.info('requesting symbol for %s', product_id)
        if product_id in self.pairs:
            return self.pairs[product_id]
        return None

    def get_market_liquidity(self, product_id, depth):
        """
        Get liquidity for product
        :param product_id:
        :param depth:
        :return:
        """
        logging.info('requesting liquidity for %s %s', product_id, depth)
        response = self.client.market.get_market_liquidity(int(product_id), int(depth))
        return {"symbol": self.get_symbol(product_id), "product_id": product_id,
                "depth": depth, "response": response}

    def execute(self, product_id, side, amount, price):
        """
        !!!SIMULATING ORDER EXECUTION
        :param product_id:
        :param side:
        :param amount:
        :param price:
        :return:
        """
        logging.info('simulating order execution for %s %s %s %s', product_id, side, amount, price)
        response = self.get_market_liquidity(product_id, 1000)

        data = {"symbol": self.get_symbol(product_id), "side": side,
                "amount": amount, "price": price}
        response.update(data)
        return response
