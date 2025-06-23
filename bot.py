from binance.client import Client
from binance.enums import *
import logging
import time
import requests


class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.logger = self.setup_logger()
        self.client = Client(api_key, api_secret)

        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
            self.client.API_URL = self.client.FUTURES_URL

        self.logger.info("Initialized Binance Futures Client (Testnet Mode)")

    def setup_logger(self):
        logging.basicConfig(
            filename='bot.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger("BinanceBot")

    def get_server_time(self):
        try:
            res = requests.get("https://testnet.binancefuture.com/fapi/v1/time")
            res.raise_for_status()
            return int(res.json()["serverTime"])
        except Exception as e:
            self.logger.error("Failed to get server time: %s", str(e))
            return int(time.time() * 1000)

    def place_market_order(self, symbol, side, quantity):
        try:
            server_time = self.get_server_time()
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side.lower() == 'buy' else SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=quantity,
                timestamp=server_time,
                recvWindow=5000
            )
            self.logger.info("Market Order: %s", order)
            return order
        except Exception as e:
            self.logger.error("Market Order Error: %s", str(e))
            return {"error": str(e)}

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            server_time = self.get_server_time()
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side.lower() == 'buy' else SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price,
                timestamp=server_time,
                recvWindow=5000
            )
            self.logger.info("Limit Order: %s", order)
            return order
        except Exception as e:
            self.logger.error("Limit Order Error: %s", str(e))
            return {"error": str(e)}

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        try:
            server_time = self.get_server_time()
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side.lower() == 'buy' else SIDE_SELL,
                type=FUTURE_ORDER_TYPE_STOP_MARKET,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                stopPrice=stop_price,
                price=limit_price,
                timestamp=server_time,
                recvWindow=5000
            )
            self.logger.info("Stop-Limit Order: %s", order)
            return order
        except Exception as e:
            self.logger.error("Stop-Limit Order Error: %s", str(e))
            return {"error": str(e)}
