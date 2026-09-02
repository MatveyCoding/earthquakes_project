from confluent_kafka import Consumer
from src.config import load_config
from src.storage.postgres import WeatherTable
import json
import time
import uuid

config = load_config()

table = WeatherTable(config)

consumer_config = {
    "bootstrap.servers": config['kafka']['bootstrap_servers'],
    "group.id": f'consumer_weather-{uuid.uuid4()}',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False  # не сохранять позицию
}

consumer = Consumer(consumer_config)

consumer.subscribe([config['kafka']['weather_topic']])

time.sleep(10)

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        break

    if msg.error():
        print(f"Ошибка:{msg.error()}")
        continue
    try:
        #превращаем json в словарь
        event = json.loads(msg.value().decode("utf-8"))
        # сохраняем сообщение в базу
        table.save_event(event)
        print(f"Сохранено:{event['event_id']}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    