import os
import requests
import json
import math
import paho.mqtt.publish as mqttpublish
from requests.exceptions import HTTPError
from datetime import datetime

millnames = ['','T','M','B','Tr']
consList=os.getenv("COINS_LIST", default = "bitcoin,ethereum,cardano,polkadot")
mqttHost=os.getenv("MQTT_HOST", default = "192.168.0.215")
mqttPort=os.getenv("MQTT_PORT", default = "1883")
mqttTopic=os.getenv("MQTT_TOPIC", default = "crypto/prices")
currency=os.getenv("CURRENCY", default = "usd")

def priceServer(): 
    prices = getPrices()
    responsePrices = createResponse(prices)
    #print('publish:', responsePrices)
    mqttpublish.single(mqttTopic, responsePrices, qos=0, retain=True, hostname=mqttHost,
        port=int(mqttPort), client_id="pricesMqtt", keepalive=60, will=None, auth=None,
        tls=None) 

def formatPrice(price):
    if price < 1:
        return "{:.2f}".format(price)
    elif price > 100 and price < 100000:
        return "{:,.0f}".format(price)
    else:
        return "{:,}".format(price)        

def getPrices():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=' + currency + '&ids=' + consList)
        response.raise_for_status()
        return response.json()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')    

def extract_volume(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return int(json['total_volume'])
    except KeyError:
        return 0

def createResponse(prices):
    data = {}
    data['time'] = datetime.now().strftime("%a %-d-%m-%y  %H:%M:%S") 
    data['coins'] = []

    prices.sort(key=extract_volume, reverse=True)

    for price in prices:
        coin = {}
        coin['name'] = price['symbol'].upper()
        coin['price'] = "$" + str(formatPrice(price['current_price']))
        coin['price_change_24h'] = str("{:.1f}".format(price['price_change_percentage_24h'])) + "%"
        coin['vol'] = millify(price['total_volume'])
        data['coins'].append(coin)
    return json.dumps(data)    

def millify(n):
    n = float(n)
    millidx = max(0, min(len(millnames)-1, int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

priceServer()
