FROM python:3.14.0-alpine3.22 
RUN apk update && apk add tzdata
ENV TZ=Australia/Melbourne
ENV MQTT_HOST=192.168.0.215
ENV COINS_LIST=bitcoin,ethereum
ENV CURRENCY=usd
ENV MQTT_PORT=1883
ENV MQTT_TOPIC=crypto/prices

COPY . .

RUN pip install -r requirements.txt
RUN crontab crontab

CMD ["crond", "-f"]