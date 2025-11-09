-- Ce script est exécuté au premier démarrage du conteneur PostgreSQL.
-- Il peut être utilisé pour créer des bases de données, des rôles, ou des schémas.

-- Création de la base de données pour Airflow si elle n'existe pas
-- Note: docker-compose crée déjà la DB principale 'meteo_agricole'
SELECT 'CREATE DATABASE airflow'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'airflow');

-- Création de la base de données pour MLflow si elle n'existe pas
SELECT 'CREATE DATABASE mlflow'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mlflow');

-- Vous pouvez ajouter d'autres commandes d'initialisation ici si nécessaire.
-- Par exemple, créer un utilisateur spécifique pour l'application :
-- CREATE USER myapp_user WITH PASSWORD 'secure_password';
-- GRANT CONNECT ON DATABASE meteo_agricole TO myapp_user;
-- GRANT USAGE ON SCHEMA public TO myapp_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO myapp_user;

-- Activer l'extension TimescaleDB dans la base de données principale
-- La connexion se fait à la DB définie par POSTGRES_DB dans docker-compose.yml
\c meteo_agricole;

CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Création des tables (gérées par SQLAlchemy dans l'application, mais peut être fait ici)
-- Note: Les tables sont créées par `Base.metadata.create_all(self.engine)` dans `load.py`.
-- Il est donc préférable de laisser l'application gérer le schéma.
-- Si vous préférez gérer le schéma ici, décommentez et adaptez les commandes ci-dessous.

/*
CREATE TABLE IF NOT EXISTS weather_records (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    temperature_celsius REAL,
    feels_like_celsius REAL,
    humidity_percent REAL,
    pressure_hpa REAL,
    wind_speed_ms REAL,
    clouds_percent REAL,
    uvi REAL,
    weather_description VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS weather_forecasts (
    id SERIAL PRIMARY KEY,
    forecast_date TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    temp_min REAL,
    temp_max REAL,
    temp_day REAL,
    humidity REAL,
    pressure REAL,
    wind_speed REAL,
    rain_mm REAL,
    pop REAL,
    uvi REAL,
    temp_amplitude REAL,
    water_stress_index REAL,
    et0_mm REAL,
    irrigation_need_mm REAL,
    disease_risk VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS agricultural_fields (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    crop_type VARCHAR(100),
    area_hectares REAL,
    metadata JSONB,
    created_at TIMESTAMTz DEFAULT NOW()
);

-- Transformer les tables en hypertables TimescaleDB
SELECT create_hypertable('weather_records', 'timestamp', if_not_exists => TRUE);
SELECT create_hypertable('weather_forecasts', 'forecast_date', if_not_exists => TRUE);
*/

-- Message de fin
\echo "Base de données initialisée, extension TimescaleDB activée."

