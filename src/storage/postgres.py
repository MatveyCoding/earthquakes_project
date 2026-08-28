from sqlalchemy import create_engine
from sqlalchemy import insert, Table, MetaData, select, func


class EarthquakeTable:

    def __init__(self, config):
        self.engine = create_engine((f"{config['storage']['type']}"
            f"://{config['storage']['user']}"
            f":{config['storage']['password']}"
            f"@{config['storage']['host']}"
            f":{config['storage']['port']}"          
            f"/{config['storage']['database']}"))
        metadata = MetaData()
        self.earthquake_table = Table(
            'earthquakes',
             metadata,
             autoload_with= self.engine
        )


    def save_event(self, event:dict):
        with self.engine.connect() as conn:
            conn.execute(insert(self.earthquake_table).values(**event))

    def get_last_data_note(self):
        with self.engine.connect() as conn:
            result = conn.execute(select(func.max(self.earthquake_table.c.event_time)))

        return result.scalar()


        

        


