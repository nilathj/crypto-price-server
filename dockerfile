FROM python:3.10.5-alpine3.16
RUN apk update && apk add tzdata
ENV TZ=Australia/Melbourne
ENV MQTT_HOST=192.168.0.215
ENV COINS_LIST=binancecoin,bitcoin,avalanche-2,ethereum,polkadot,cardano,matic-network,cosmos,mina-protocol,optimism
ENV CURRENCY=usd
ENV MQTT_PORT=1883
ENV MQTT_TOPIC=crypto/prices

COPY . .

RUN pip install -r requirements.txt
RUN crontab crontab

CMD ["crond", "-f"]