-- Таблица землетрясений
CREATE TABLE IF NOT EXISTS earthquakes (
    id SERIAL PRIMARY KEY,
    event_id TEXT UNIQUE,
    magnitude DECIMAL(3,1) NOT NULL,
    place VARCHAR(300),
    event_time TIMESTAMP,
    tsunami BOOLEAN,
    sig INT,
    count_of_stations INT,
    mean_square_error DECIMAL(3,1),
    latitude DECIMAL(8,5),
    longitude DECIMAL(8,5),
    depth_km DECIMAL(7,2),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Исторические землетрясения
CREATE TABLE IF NOT EXISTS earthquakes_historic (
    id SERIAL PRIMARY KEY,
    event_id TEXT UNIQUE,
    magnitude DECIMAL(3,1) NOT NULL,
    place VARCHAR(300),
    event_time TIMESTAMP,
    tsunami BOOLEAN,
    sig INT,
    count_of_stations INT,
    mean_square_error DECIMAL(3,1),
    latitude DECIMAL(8,5),
    longitude DECIMAL(8,5),
    depth_km DECIMAL(7,2),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Погода
CREATE TABLE IF NOT EXISTS weather_table (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP,
    longitude DECIMAL(8,5),
    latitude DECIMAL(8,5),
    temperature DECIMAL(5,2),
    wind_speed DECIMAL(5,2),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Результат джойна погоды и землетрясений
CREATE TABLE IF NOT EXISTS earthquake_weather_join (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(50),
    place VARCHAR(300),
    magnitude DECIMAL(4,1),
    latitude DECIMAL(8,5),
    longitude DECIMAL(8,5),
    temperature DECIMAL(5,2),
    wind_speed DECIMAL(5,2),
    weather_time TIMESTAMP,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы
CREATE INDEX IF NOT EXISTS idx_earthquakes_time ON earthquakes(event_time);
CREATE INDEX IF NOT EXISTS idx_earthquakes_place ON earthquakes(place);
CREATE INDEX IF NOT EXISTS idx_weather_time ON weather_table(time);
CREATE INDEX IF NOT EXISTS idx_weather_lat_lon ON weather_table(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_join_place ON earthquake_weather_join(place);