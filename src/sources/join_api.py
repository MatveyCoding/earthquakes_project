from src.storage.postgres import EarthquakeTable
from src.storage.postgres import WeatherTable
from sqlalchemy import join, select, insert
from sqlalchemy import and_, func, Table, MetaData
from src.config import load_config


def run_join():
    config = load_config()

    et = EarthquakeTable(config)

    wt = WeatherTable(config)

    metadata = MetaData()

    join_table = Table(
    'earthquake_weather_join',
        metadata,
        autoload_with=et.engine
    )


    with wt.engine.begin() as conn:
        result = conn.execute(
                    select(et.earthquake_table.c.event_id,
                                    et.earthquake_table.c.place,
                                    et.earthquake_table.c.magnitude,
                                    et.earthquake_table.c.latitude,
                                    wt.weather_table.c.temperature,
                                    wt.weather_table.c.wind_speed,
                                    wt.weather_table.c.time 
                                    ).select_from( wt.weather_table.join
                                    (
                                        et.earthquake_table,
                                        and_(
                                        func.round(et.earthquake_table.c.latitude, 2) ==  func.round(wt.weather_table.c.latitude,2),
                                        func.round(et.earthquake_table.c.longitude,2) == func.round(wt.weather_table.c.longitude,2) 
                                        ),
                                        isouter=True
                                    )))
        rows = result.fetchall()

        for row in rows:
            conn.execute(join_table.insert().values(
                event_id=row.event_id,
                place=row.place,
                magnitude=row.magnitude,
                latitude=row.latitude,
                temperature=row.temperature,
                wind_speed=row.wind_speed,
                weather_time=row.time
            ))
        
       
    