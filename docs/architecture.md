# Architecture Technique

## Vue d'Ensemble

La plateforme d'Intelligence Météo & Agricole suit une architecture en 3 couches :

1. **Couche Data Engineering** : ETL automatisé pour collecte et stockage de données
2. **Couche Data Science** : Modèles ML pour prédictions et recommandations
3. **Couche Application** : API et interfaces utilisateur

---

## 1. Data Engineering - Pipeline ETL

### Sources de Données

#### OpenWeather One Call API 3.0
- **URL** : `https://api.openweathermap.org/data/3.0/onecall`
- **Données** : Météo actuelle + prévisions 7 jours
- **Fréquence** : Quotidienne (6h00)
- **Format** : JSON

#### FAO/FAOSTAT
- **URL** : `https://fenixservices.fao.org/faostat/api/v1`
- **Données** : Productions agricoles, rendements
- **Fréquence** : Mensuelle
- **Format** : JSON/CSV

#### Copernicus (optionnel)
- **Données** : Humidité des sols, indices de végétation
- **Format** : NetCDF/GeoTIFF

### Pipeline ETL (Airflow)

```
┌──────────────┐
│   EXTRACT    │  → Récupération APIs (extract.py)
└──────┬───────┘
       │
┌──────▼───────┐
│  TRANSFORM   │  → Nettoyage & enrichissement (transform.py)
└──────┬───────┘
       │
┌──────▼───────┐
│     LOAD     │  → Stockage PostgreSQL (load.py)
└──────────────┘
```

### Base de Données (PostgreSQL + TimescaleDB)

**Tables principales :**

1. `weather_records` : Données météo historiques
2. `weather_forecasts` : Prévisions météo
3. `agricultural_fields` : Champs agricoles enregistrés
4. `predictions` : Prédictions ML stockées

**Schéma `weather_forecasts` :**
```sql
CREATE TABLE weather_forecasts (
    id SERIAL PRIMARY KEY,
    forecast_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    temp_min FLOAT,
    temp_max FLOAT,
    humidity FLOAT,
    rain_mm FLOAT,
    -- Features dérivées
    irrigation_need_mm FLOAT,
    water_stress_index FLOAT,
    disease_risk VARCHAR(20)
);

-- Index TimescaleDB pour séries temporelles
CREATE INDEX ON weather_forecasts (forecast_date DESC);
```

---

## 2. Data Science - Modèles ML

### Feature Engineering

**Features météo brutes :**
- Température (min, max, moyenne)
- Humidité (%)
- Précipitations (mm)
- Pression atmosphérique
- Vitesse du vent
- Couverture nuageuse

**Features dérivées :**
```python
# Amplitude thermique
temp_amplitude = temp_max - temp_min

# Index de stress hydrique
water_stress_index = (temp_max - 25) * (100 - humidity) / 100

# Évapotranspiration (ET0) - Hargreaves
et0_mm = 0.0023 * (temp_mean + 17.8) * temp_amplitude^0.5

# Besoin en irrigation
irrigation_need = max(0, et0_mm - rain_mm)

# Risque maladies
disease_risk = "high" if (humidity > 70 and 15 < temp < 30) else "low"
```

### Modèles Prédictifs

#### 1. Prédiction Pluie (Prophet + XGBoost)

**Objectif** : Prédire probabilité et quantité de pluie à J+1, J+3, J+7

**Algorithme** :
- Prophet (séries temporelles) pour tendances saisonnières
- XGBoost pour précision court terme

**Features** :
- Historique pluie 30 jours
- Température, humidité, pression
- Saison, mois

**Métrique** : RMSE < 5mm

#### 2. Détection Sécheresse (Random Forest)

**Objectif** : Classifier niveau de sécheresse (aucune, modérée, sévère)

**Features** :
- Cumul pluie 30/60/90 jours
- Index de stress hydrique
- Historique ET0

**Métrique** : F1-Score > 0.85

#### 3. Risque Maladies (Classification)

**Objectif** : Détecter conditions favorables aux maladies fongiques

**Règles métier** :
```python
if humidity > 80 and 18 < temperature < 28:
    risk = "HIGH"
elif humidity > 60 and 15 < temperature < 30:
    risk = "MEDIUM"
else:
    risk = "LOW"
```

### MLOps

**MLflow** :
- Tracking expérimentations
- Versioning modèles
- Registry modèles production

**Déploiement** :
- Models packagés avec joblib/pickle
- API FastAPI expose modèles
- Dockerisation pour portabilité

---

## 3. Application - Backend & Frontend

### Backend API (FastAPI)

**Architecture** :
```
src/api/
├── main.py           # Point d'entrée
├── routers/
│   ├── weather.py    # Endpoints météo
│   ├── predictions.py # Endpoints ML
│   └── notifications.py # Twilio SMS/WhatsApp
├── database.py       # Connexion DB
└── config.py         # Configuration
```

**Endpoints principaux** :

```
GET  /api/weather/current?lat=&lon=
GET  /api/weather/forecast?lat=&lon=&days=7
GET  /api/predictions/irrigation?lat=&lon=
GET  /api/predictions/disease-risk?lat=&lon=
POST /api/fields
POST /api/notifications/sms
```

**Authentification** : JWT (optionnel)

### Frontend (React)

**Composants** :
- Dashboard météo (Plotly charts)
- Carte interactive (Leaflet)
- Formulaire enregistrement champ
- Notifications

### Notifications (Twilio)

**SMS/WhatsApp** :
```python
client.messages.create(
    body="Alerte: Risque de pluie demain. Pas besoin d'irrigation.",
    from_="+1234567890",
    to="+221701234567"
)
```

---

## Déploiement

### Docker Compose

**Services** :
- `postgres` : Base de données
- `redis` : Cache & queue
- `airflow-webserver` : Interface Airflow
- `airflow-scheduler` : Orchestration DAGs
- `api` : Backend FastAPI
- `mlflow` : Tracking ML
- `frontend` : Application React

### CI/CD (GitHub Actions)

**Pipeline** :
1. Tests unitaires (pytest)
2. Linting (black, flake8)
3. Build Docker images
4. Déploiement production (si main)

---

## Sécurité

- Variables d'environnement (.env) pour secrets
- HTTPS en production
- Rate limiting API
- Validation Pydantic
- CORS configuré

---

## Performance

- Cache Redis pour requêtes fréquentes
- Index PostgreSQL sur colonnes recherchées
- TimescaleDB pour optimisation séries temporelles
- Compression réponses API (gzip)

---

## Monitoring

- Logs structurés (Loguru)
- Métriques Airflow
- Health checks endpoints
- Grafana (optionnel)

---

## Scalabilité

- Airflow Celery pour parallélisation
- API stateless (horizontal scaling)
- PostgreSQL réplication (lecture)
- CDN pour frontend statique

---

Dernière mise à jour : 2024
