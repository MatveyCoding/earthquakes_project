import requests as req
from src.config import load_config
from datetime import datetime

class USGSSource:
    def get_info(self):
        config = load_config()
        now = datetime.now().strftime("%Y-%m-%d")
        usgs_resp = req.get(f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2026-07-21&endtime={now}")
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
            'event_time': datetime.fromtimestamp(properties['time'] / 1000),
            'tsunami': bool(properties['tsunami']),
            'sig': properties['sig'],
            'nst':properties['nst'],
            'rms': properties['rms'],
            'longitude': coordinates[0],
            'latitude': coordinates[1],
            'depth_km': coordinates[2]


        }
      