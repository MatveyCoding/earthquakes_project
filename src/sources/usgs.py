import requests as req
from src.config import load_config
from datetime import datetime, timedelta
from src.storage.postgres import EarthquakeTable

class USGSSource:
    def __init__(self):
        table = EarthquakeTable(load_config())

        last_data = table.get_last_data_note()
        now = datetime.now()
        hour = now.hour if (now.hour%2 ==0) else now.hour - 1
        now = now.replace(hour=hour, minute=0, second=0, microsecond=0)

        if last_data:
            self.start_date = last_data
            self.end_date = now
        else:
            self.start_date = now - timedelta(days=1)
            self.end_date = now 
        
            #self.start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


    def get_info(self):
        config = load_config()
        start = self.start_date.strftime("%Y-%m-%dT%H:%M:%S")
        end = self.end_date.strftime("%Y-%m-%dT%H:%M:%S")
        usgs_resp = req.get(f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start }&endtime={end}")
        dict_resp = usgs_resp.json()
        result = []

        for feature in dict_resp['features']:
            result.append(self.extract_params(feature))
        return result

        
    def extract_params(self, features):
        properties = features['properties']
        coordinates = features['geometry']['coordinates']

        return {
            'event_id': features['id'],
            'magnitude': properties['mag'],
            'place': properties['place'],
            'event_time': datetime.fromtimestamp(properties['time'] / 1000).isoformat(),
            'tsunami': bool(properties['tsunami']),
            'sig': properties['sig'],
            'count_of_stations':properties['nst'],
            'mean_square_error': properties['rms'],
            'longitude': coordinates[0],
            'latitude': coordinates[1],
            'depth_km': coordinates[2]


        }
      