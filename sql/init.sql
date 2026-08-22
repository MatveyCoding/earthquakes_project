CREATE TABLE IF NOT EXISTS earthquakes(
    id SERIAL PRIMARY KEY,
    event_id TEXT UNIQUE,
    magnitude DECIMAL(3,1) NOT NULL,  
    place VARCHAR(300),
    event_time TIMESTAMP,
    tsunami BOOLEAN,
    sig INT,
    ids TEXT,
    count_of_stations INT,
    mean_square_error DECIMAL(3,1),
    latitude DECIMAL(8,5),
    longitude DECIMAL(8,5),
    depth_km DECIMAL(7,2),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS id_index ON earthquakes(id);
CREATE INDEX IF NOT EXISTS place_index ON earthquakes(place);
CREATE INDEX IF NOT EXISTS event_time_index ON earthquakes(event_time);


