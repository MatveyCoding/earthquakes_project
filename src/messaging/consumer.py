from confluent_kafka import Consumer
from src.config import load_config
from src.storage.postgres import EarthquakeTable
import json

#забираем обычный конфиг
config = load_config() 
#инициализируем кафка-конфиг для коснюмера
consumer_config = {
    "bootstrap.servers": config['kafka']['bootstrap_servers'],
    "group.id": 'earthquake-consumer',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)
# по топику подписываемся на соответсвуюзий продюссер
consumer.subscribe([config['kafka']['topic']])

Earthquakes = EarthquakeTable(config)
while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print(f"Ошибка: {msg.error()}")
        continue
    try:
        event = json.loads(msg.value().decode("utf-8"))
        Earthquakes.save_event(event)
        print(f"Сохранено:{event['event_id']}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

