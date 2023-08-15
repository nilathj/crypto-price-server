# Docker MQTT Crypto price server
This is a docker container that executes a python script from a cron job every 5 minutes.
The python script fetches the price and volume data for a list of crypto currencies using the coingecko api.  These prices are published to a MQTT topic as a JSON payload periodically.  These MQTT messages can then be consumed by the MQTT Crypto price tracker client using an ESP32-TTGO-T4 display.

## Prerequisites
* MQTT server and topic setup.  I have used the [Mosquitto MQTT server](https://mosquitto.org/)
* Docker needs to be installed to run the docker container.

## Structure of the JSON payload in the MQTT message
```
{
   "time":"Sat 1-04-23  19:09:15",
   "coins":[
      {
         "name":"BTC",
         "price":"$28,451",
         "price_change_24h":"2.2%",
         "vol":"17B"
      },
      {
         "name":"ETH",
         "price":"$1,825",
         "price_change_24h":"1.5%",
         "vol":"10B"
      },
      {
         "name":"ADA",
         "price":"$0.39",
         "price_change_24h":"1.4%",
         "vol":"759M"
      },
      {
         "name":"DOT",
         "price":"$6.26",
         "price_change_24h":"0.6%",
         "vol":"202M"
      }
   ]
}
```

## Build docker image
```
docker build --tag crypto-server .
```

## Running the image
Supported Env arguments
| ENV name | Description | Default Value |
|----------|-------------|---------------|
| TZ       | Timezone | Australia/Melbourne|
| MQTT_HOST| IP address of MQTT server| 192.168.0.215 |
| MQTT_PORT| MQTT port | 1883 |
| MQTT_TOPIC | MQTT topic that the price data is published to | crypto/prices |
| COINS_LIST| Comma separated list of coingecko supported crypto currency ids| binancecoin,bitcoin,avalanche-2,ethereum,polkadot,cardano,matic-network,cosmos,mina-protocol,optimism |
| CURRENCY | price display currency | usd |

## Coingecko supported coins list
To get a list of coingecko supported coins use their API documentation for GET /coins/list:
```
https://www.coingecko.com/en/api/documentation
```
