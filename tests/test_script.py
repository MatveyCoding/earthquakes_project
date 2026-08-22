from src.storage.postgres import EarthquakeTable
from src.config import load_config
import time

test_event = {
    'event_id': 'test123',
    'magnitude': 3.5,
    'place': 'Test Location',
    'event_time': '2026-08-22 10:00:00',
    'latitude': 19.6,
    'longitude': -155.2,
    'depth_km': 35.4,
    'tsunami': False
}


config = load_config()
print(f"Грузим конфиг:\n{config}")

Earthquakes = EarthquakeTable(config)

time.sleep(5)

print("Запущен процесс получения данных")

Earthquakes.save_event(test_event)





