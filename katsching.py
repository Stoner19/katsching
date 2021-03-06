#!/usr/bin/python2.7

import time
from bittrex import *

def timestamp(s):
    from dateutil.parser import parse
    return parse(s['TimeStamp']).strftime("%Y-%m-%d %H:%M:%S:%f")

def play_sound(sound):
    from pygame import mixer
    mixer.init()
    mixer.music.load(sound)
    mixer.music.play()
    time.sleep(1)
    mixer.quit()

b = Bittrex('API_KEY', 'API_SECRET')
sales = []
buys = []
orders = b.api_query('getorderhistory')
for order in orders['result']:
    if order['OrderType'] == 'LIMIT_SELL':
        sales.append(order)
    if order['OrderType'] == 'LIMIT_BUY':
        buys.append(order)
play_sound('katsching.wav')

while True:
    try:
        new_sales = []
        new_buys = []
        orders = b.api_query('getorderhistory')['result']
        for order in orders:
            if order['OrderType'] == 'LIMIT_SELL':
                if order not in sales:
                    new_sales.append(order)
            if order['OrderType'] == 'LIMIT_BUY':
                if order not in buys:
                    new_buys.append(order)

        if len(new_buys) or len(new_sales):
            total = 0
            summaries = b.get_market_summaries()['result']
            balances = b.get_balances()['result']
            for bal in balances:
                if bal['Currency'] != 'BTC':
                    total += bal['Balance'] * filter(lambda x: x['MarketName'] == 'BTC-'+bal['Currency'], summaries)[0]['Ask']
                else:
                    total += bal['Balance']

            if len(new_sales):
                play_sound('katsching.wav')
            if len(new_buys):
                play_sound('nomnom.wav')

            for order in new_sales:
                print timestamp(order), "Sold  ", ("%0.08f" % order['Quantity']).rjust(12), order['Exchange'].replace('BTC-', ''), '@', "%0.08f" % order['PricePerUnit'], "total @", total
                sales.append(order)
            for order in new_buys:
                print timestamp(order), "Bought", ("%0.08f" % order['Quantity']).rjust(12), order['Exchange'].replace('BTC-', ''), '@', "%0.08f" % order['PricePerUnit'], "total @", total
                buys.append(order)
    except Exception, e:
        print e
    time.sleep(10)

