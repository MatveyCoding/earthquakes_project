from confluent_kafka import Producer
from src.config import load_config
from src.sources.usgs import USGSSource
from datetime import datetime
import time
import json

def activate_producer():
    #инициализируем класс получаения данных с сервиса
    usgs_data = USGSSource()
    config = load_config()
    #конфиг продюссера
    kafka_conf_prod =  {
        "bootstrap.servers": config['kafka']['bootstrap_servers'],
        "client.id": "earthquake",
        "enable.idempotence": True, #предотвращаем дубли
        "acks": "all", # ждём подтверждения от всех реплик
        "retries": 100,
        "max.in.flight.requests.per.connection": 1 #поддерживаем идемпотентность
    }

    producer = Producer(kafka_conf_prod)

    get_id = "get_request"



    # получаем список json файлов
    json_list = usgs_data.get_info()

    for list_element_json in json_list:
        producer.produce(
            topic = config['kafka']['topic'], 
            key = get_id.encode("utf-8"),
            value = json.dumps(list_element_json).encode("utf-8")# потом поменять test_json

        )
    producer.flush()
    time.sleep(5)
    