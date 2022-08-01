#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config
import websocket
import pprint
import json
import numpy as np
import talib

from binance.client import Client
from binance.enums import *

SYMBOL = 'ethusdt'
TIMEFRAME = '1m'
SOCKET = f'wss://stream.binance.com:9443/ws/{SYMBOL}@kline_{TIMEFRAME}'

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.05

closes = []
in_position = False

client = Client(config.API_KEY, config.API_SECRET)

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes
    print('received message')
    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print(f'candle closed at {close}')
        closes.append(float(close))
        print('closes')
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = np.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print('all rsis calculated so far')
            print(rsi)
            last_rsi = rsi[-1]
            print(f'the current rsi is {last_rsi}')

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print('Overbought! Sell! Sell! Sell!')
                    # put binance sell order logic here
                else:
                    print("It is overbought, but you don't own any, nothing to do.")

            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("It is oversold, but you already own it, nothing to do.")
                else:
                    print('Oversold! Buy! Buy! Buy!')
                    # put binance buy order logic here

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()