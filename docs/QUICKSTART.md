# Guide de Démarrage Rapide

## Prérequis

- Python 3.10+
- Docker & Docker Compose
- Git
- Compte OpenWeather (clé API gratuite)

---

## Installation en 5 Minutes

### 1. Cloner le repository

```bash
git clone <url-du-repo>
cd hackathon-meteo-agricole
```

### 2. Configuration environnement

```bash
# Copier .env.example
cp .env.example .env

# Éditer .env et ajouter votre clé OpenWeather
nano .env  # ou vim, code, etc.
```

**Variables critiques à configurer :**
```env
OPENWEATHER_API_KEY=votre_cle_api_ici
```

Obtenir une clé API gratuite : https://openweathermap.org/api

### 3. Lancer avec Docker

```bash
# Construire et démarrer tous les services
docker-compose up -d

# Vérifier que tout fonctionne
docker-compose ps
```

**Services disponibles :**
- API Backend : http://localhost:8000
- API Docs : http://localhost:8000/docs
- Airflow UI : http://localhost:8080 (user: admin, pass: admin)
- MLflow : http://localhost:5000

### 4. Tester l'API

```bash
# Health check
curl http://localhost:8000/health

# Météo actuelle Dakar
curl "http://localhost:8000/api/weather/current?latitude=14.7167&longitude=-17.4677"

# Prévisions 7 jours
curl "http://localhost:8000/api/weather/forecast?latitude=14.7167&longitude=-17.4677&days=7"

# Recommandations irrigation
curl "http://localhost:8000/api/predictions/irrigation?latitude=14.7167&longitude=-17.4677"
```

---

## Développement Local (Sans Docker)

### 1. Environnement virtuel Python

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. PostgreSQL local

```bash
# Installer PostgreSQL
sudo apt install postgresql  # Linux
brew install postgresql  # Mac

# Créer base de données
createdb meteo_agricole

# Configurer .env
DATABASE_URL=postgresql://user:password@localhost:5432/meteo_agricole
```

### 3. Lancer l'API

```bash
cd src
uvicorn api.main:app --reload --port 8000
```

### 4. Tests

```bash
pytest tests/ -v
```

---

## Utilisation Rapide

### Créer un champ agricole

```bash
curl -X POST "http://localhost:8000/api/fields" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mon Champ de Riz",
    "latitude": 14.7167,
    "longitude": -17.4677,
    "crop_type": "riz",
    "area_hectares": 3.5
  }'
```

### Obtenir prévisions avec recommandations

```python
import requests

# Prévisions météo
response = requests.get(
    "http://localhost:8000/api/weather/forecast",
    params={"latitude": 14.7167, "longitude": -17.4677, "days": 7}
)
forecasts = response.json()

# Recommandations irrigation
response = requests.get(
    "http://localhost:8000/api/predictions/irrigation",
    params={"latitude": 14.7167, "longitude": -17.4677}
)
irrigation = response.json()
print(irrigation)
```

---

## Airflow - ETL Automatisé

### Accéder à Airflow

1. Ouvrir http://localhost:8080
2. Login : `admin` / `admin`
3. Activer le DAG `weather_etl_pipeline`

Le DAG s'exécute automatiquement tous les jours à 6h00.

### Lancer manuellement

```bash
# Via l'interface Airflow UI
# ou via CLI :
docker-compose exec airflow-webserver airflow dags trigger weather_etl_pipeline
```

---

## Développer & Contribuer

### Créer une branche feature

```bash
git checkout -b feature/ma-nouvelle-fonctionnalite
```

### Formater le code

```bash
black src/
isort src/
flake8 src/
```

### Commit & Push

```bash
git add .
git commit -m "feat: Ajout de nouvelle fonctionnalité"
git push origin feature/ma-nouvelle-fonctionnalite
```

### Créer Pull Request

Sur GitHub, créer une PR depuis votre branche vers `main`

---

## Troubleshooting

### Problème : Port déjà utilisé

```bash
# Changer les ports dans docker-compose.yml
ports:
  - "8001:8000"  # Au lieu de 8000:8000
```

### Problème : Erreur connexion PostgreSQL

```bash
# Vérifier que le service est démarré
docker-compose ps postgres

# Voir les logs
docker-compose logs postgres
```

### Problème : Clé API OpenWeather invalide

```bash
# Vérifier que la clé est bien dans .env
cat .env | grep OPENWEATHER_API_KEY

# Tester manuellement la clé
curl "https://api.openweathermap.org/data/3.0/onecall?lat=14.7167&lon=-17.4677&appid=VOTRE_CLE"
```

---

## Prochaines Étapes

1. Explorer la documentation API : http://localhost:8000/docs
2. Tester les notebooks Jupyter dans `/notebooks`
3. Configurer les notifications Twilio (SMS/WhatsApp)
4. Développer le frontend React
5. Entraîner les modèles ML

---

Pour plus d'informations, consulter :
- [Architecture complète](architecture.md)
- [README principal](../README.md)
- [Documentation API](http://localhost:8000/docs)
