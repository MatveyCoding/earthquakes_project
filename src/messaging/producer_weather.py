from confluent_kafka import Producer
from src.config import load_config
from src.sources.weather import Weather_info
from datetime import datetime
from src.storage.postgres import EarthquakeTable
import time
import json

def activate_producer():

    config = load_config()

    earthquake_table = EarthquakeTable(config)

    weather_data = Weather_info()

    

    kafka_conf_prod =  {
            "bootstrap.servers": config['kafka']['bootstrap_servers'],
            "client.id": "weather",
            "enable.idempotence": True, #предотвращаем дубли
            "acks": "all", # ждём подтверждения от всех реплик
            "retries": 100,
            "max.in.flight.requests.per.connection": 1 #поддерживаем идемпотентность
        }
    
    producer = Producer(kafka_conf_prod)

    get_id = "weather_get_requsest"
    json_list = []
    latitudes, longitudes = earthquake_table.get_columns(['latitude', 'longitude'])
    for i in range(100):                                  #(len(latitudes)):
        json_list.append(weather_data.get_info(latitudes[i], longitudes[i]))
        time.sleep(1)

    for list_element_json in json_list:
            producer.produce(
                topic = config['kafka']['weather_topic'], 
                key = get_id.encode("utf-8"),
                value = json.dumps(list_element_json, default=str).encode("utf-8")# потом поменять test_json
    
            )
    producer.flush()
    time.sleep(5)




