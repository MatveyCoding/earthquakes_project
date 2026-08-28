from confluent_kafka import Consumer
from src.config import load_config
from src.storage.postgres import EarthquakeTable
import json
import time
import uuid

config = load_config()

consumer_config = {
    "bootstrap.servers": config['kafka']['bootstrap_servers'],
    "group.id": f'consumer-{uuid.uuid4()}',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False  # не сохранять позицию
}

consumer = Consumer(consumer_config)
consumer.subscribe([config['kafka']['topic']])
time.sleep(10)  
Earthquakes = EarthquakeTable(config)

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        break

    if msg.error():
        print(f"Ошибка: {msg.error()}")
        continue

    try:
        event = json.loads(msg.value().decode("utf-8"))
        Earthquakes.save_event(event)
        print(f"Сохранено:{event['event_id']}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

consumer.close()
print("Consumer завершён")