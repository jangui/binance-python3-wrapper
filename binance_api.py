#!/usr/bin/env python3
import requests
import json

api_key = ""
api_secret = ""
api_url_base = "https://www.binance.com"

def get_prices():
    """Get lastest prices for all coins"""
    api_url = api_url_base + "/api/v1/ticker/allPrices"
    response = requests.get(api_url)
    if response.status_code == 200:
        dict_list = json.loads(response.content.decode("utf-8"))
        return {d['symbol']:d['price'] for d in dict_list}
    else:
        print("[%d] Error getting prices." % response.status_code)
        return None

def get_price(symbol):
    """
    Get latest price for a coin
    symbol = str"
    """
    prices = get_prices()
    if prices:
        return prices[symbol]

def get_tickers():
    """Get best price/quantity for all coins"""
    api_url = api_url_base + "/api/v1/ticker/allBookTickers"
    response = requests.get(api_url)
    if response.status_code == 200:
        dict_list = json.loads(response.content.decode("utf-8"))
        return {d['symbol'] : {
            'bid' : d['bidPrice'],
            'ask' : d['askPrice'],
            'bid_qty' : d['bidQty'],
            'ask_qty' : d['askQty']
            } for d in dict_list}
    else:
        print("[%d] Error getting tickers." % response.status_code)
        return None

def get_ticker(symbol):
    """
    Get best price/quantity for a coin
    symbol = str
    """
    d = get_tickers()
    if d:
        return d[symbol]


def get_depth(symbol, limit=100):
    """
    Get order book
    symbol = str
    limit = int (must be 5, 10, 20, 50, 100, 200, or 500)
    """
    options = {'symbol' : symbol, 'limit' : limit}
    api_url = api_url_base + "/api/v1/depth"
    response = requests.get(api_url, params=options)
    if response.status_code == 200:
        dict_list = json.loads(response.content.decode("utf-8"))
        return {
        "bids": {px: qty for px, qty, null in dict_list["bids"]},
        "asks": {px: qty for px, qty, null in dict_list["asks"]}
            }
    else:
        print("[%d] Error getting order book." % response.status_code)
        return None


def get_klines(symbol, interval, limit=500): #CURRENTLY NOT WORKING
    """
    Get klines / candlestick bars

    symbol = str
    interval = str
    limit = int (max 500)
    """
    options = {'symbol': symbol, 'interval' : interval, 'limit' : limit}
    api_url = api_url_base + "/api/v1/klines"
    response = requests.get(api_url, params=options)
    if response.status_code == 200:
        dict_list = json.loads(response.content.decode("utf-8"))
        return [{
        "openTime": d[0],
        "open": d[1],
        "high": d[2],
        "low": d[3],
        "close": d[4],
        "volume": d[5],
        "closeTime": d[6],
        "quoteVolume": d[7],
        "numTrades": d[8],
        } for d in dict_list]

    else:
        print("[%d] Error getting k lines." % response.status_code)
        return None


def get_balances():
    """Gets current balances"""
    api_url = api_url_base + "/api/v3/account"

