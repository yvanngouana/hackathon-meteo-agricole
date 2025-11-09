# Plateforme d'Intelligence Météo & Agricole

## 🌾 Hack2Hire - Édition 2

**Développeur :** Yvan NGOUANA

**Rôles :**
- Data Engineer Lead
- Data Scientist / ML Engineer
- Full Stack Data Engineer

---

## 📋 Description du Projet

Plateforme intelligente d'aide à la décision agricole combinant :
- Prévisions météo locales adaptées aux champs agricoles
- Modèles prédictifs (pluie, sécheresse, maladies)
- Application accessible (web/mobile + SMS/WhatsApp)

**Objectif :** Aider les agriculteurs à mieux planifier semis, arrosage et récoltes pour améliorer rendement et réduire les pertes.

---

## 🏗️ Architecture

### Stack Technique

**Data Engineering**
- Python 3.10+
- Apache Airflow (orchestration)
- PostgreSQL + TimescaleDB (stockage)
- Docker & Docker Compose

**Data Science & ML**
- scikit-learn, XGBoost
- Prophet (séries temporelles)
- MLflow (tracking)
- Pandas, NumPy

**Backend**
- FastAPI
- SQLAlchemy
- Pydantic

**Frontend**
- React + TypeScript
- Plotly (visualisation)
- Tailwind CSS

**Notifications**
- Twilio (SMS/WhatsApp)

### Schéma Architecture

```
┌─────────────────────────────────────────────────────┐
│           Sources de Données                        │
│  OpenWeather | FAO/FAOSTAT | Copernicus | IoT      │
└──────────────────┬──────────────────────────────────┘
                   │
         ┌─────────▼─────────┐
         │   ETL Pipeline    │
         │  (Apache Airflow) │
         └─────────┬─────────┘
                   │
         ┌─────────▼─────────┐
         │   PostgreSQL +    │
         │   TimescaleDB     │
         └─────────┬─────────┘
                   │
         ┌─────────▼─────────┐
         │  Modèles ML/AI    │
         │  (scikit-learn,   │
         │   XGBoost)        │
         └─────────┬─────────┘
                   │
         ┌─────────▼─────────┐
         │   API FastAPI     │
         └─────────┬─────────┘
                   │
    ┌──────────────┴──────────────┐
    │                             │
┌───▼────┐              ┌─────────▼─────┐
│  Web   │              │ SMS/WhatsApp  │
│ React  │              │    Twilio     │
└────────┘              └───────────────┘
```

---

## 🚀 Installation

### Prérequis

- Python 3.10+
- Docker & Docker Compose
- Git
- Node.js 18+ (pour frontend)

### Setup Environnement

1. **Cloner le repository**
```bash
git clone <url-du-repo>
cd hackathon-meteo-agricole
```

2. **Créer environnement virtuel Python**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration des variables d'environnement**
```bash
cp .env.example .env
# Éditer .env avec vos clés API
```

5. **Lancer avec Docker**
```bash
docker-compose up -d
```

---

## 📦 Structure du Projet

```
hackathon-meteo-agricole/
├── README.md
├── requirements.txt
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── data/
│   ├── raw/              # Données brutes
│   ├── processed/        # Données transformées
│   └── models/           # Modèles ML entraînés
│
├── src/
│   ├── etl/
│   │   ├── __init__.py
│   │   ├── extract.py    # Extraction données APIs
│   │   ├── transform.py  # Transformation & nettoyage
│   │   └── load.py       # Chargement PostgreSQL
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── rain_prediction.py      # Modèle prédiction pluie
│   │   ├── drought_detection.py    # Modèle sécheresse
│   │   └── disease_risk.py         # Modèle risques maladies
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py       # Point d'entrée FastAPI
│   │   ├── config.py
│   │   ├── database.py
│   │   └── routers/
│   │       ├── weather.py
│   │       ├── predictions.py
│   │       └── notifications.py
│   │
│   └── frontend/
│       ├── public/
│       ├── src/
│       │   ├── components/
│       │   ├── pages/
│       │   └── App.tsx
│       └── package.json
│
├── airflow/
│   ├── dags/
│   │   └── weather_etl_dag.py
│   └── config/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
│
├── tests/
│   ├── test_etl.py
│   ├── test_models.py
│   └── test_api.py
│
├── docs/
│   ├── architecture.md
│   ├── api_documentation.md
│   └── screenshots/
│
├── team/
│   ├── cv_membre1.pdf
│   ├── cv_membre2.pdf
│   └── cv_membre3.pdf
│
├── lms/
│   └── quiz_results.pdf
│
└── presentation/
    └── slides_finale.pdf
```

---

## 🎯 Fonctionnalités

### Phase 1 - Data Engineering (Jours 1-2)
- [x] Pipeline ETL automatisé avec Airflow
- [x] Connexion API OpenWeather One Call 3.0
- [x] Intégration données FAO/Copernicus
- [x] Stockage PostgreSQL/TimescaleDB

### Phase 2 - Data Science (Jours 3-4)
- [x] Modèle prédiction pluie (Prophet/XGBoost)
- [x] Modèle détection sécheresse
- [x] Modèle risques maladies agricoles
- [x] Validation & métriques performance

### Phase 3 - Application (Jours 5-7)
- [x] API Backend FastAPI
- [x] Interface web React
- [x] Visualisations météo (Plotly)
- [x] Notifications SMS/WhatsApp (Twilio)
- [x] Interface multilingue

### Phase 4 - MLOps (Jours 8-9)
- [x] Dockerisation complète
- [x] CI/CD GitHub Actions
- [x] MLflow tracking
- [x] Tests automatisés

### Phase 5 - Déploiement (Jour 10)
- [x] Déploiement production
- [x] Documentation complète
- [x] Vidéo démo

---

## 🔧 Configuration

### Variables d'Environnement (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/meteo_agricole

# APIs
OPENWEATHER_API_KEY=your_key_here
FAO_API_KEY=your_key_here

# Twilio
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890

# MLflow
MLFLOW_TRACKING_URI=http://localhost:5000

# App
APP_ENV=development
SECRET_KEY=your_secret_key
```

---

## 🚀 Lancement

### Backend API

```bash
cd src/api
uvicorn main:app --reload --port 8000
```

API accessible sur : `http://localhost:8000`
Documentation : `http://localhost:8000/docs`

### Frontend

```bash
cd src/frontend
npm install
npm run dev
```

Application web : `http://localhost:3000`

### Airflow

```bash
docker-compose up airflow
```

Airflow UI : `http://localhost:8080`

---

## 🧪 Tests

```bash
# Tests unitaires
pytest tests/

# Tests avec couverture
pytest --cov=src tests/

# Tests API
pytest tests/test_api.py -v
```

---

## 📊 Utilisation

### 1. Enregistrer un champ agricole

```bash
curl -X POST "http://localhost:8000/api/fields" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Champ Nord",
    "latitude": 14.7167,
    "longitude": -17.4677,
    "crop_type": "riz",
    "area_hectares": 2.5
  }'
```

### 2. Obtenir prévisions météo

```bash
curl "http://localhost:8000/api/weather/forecast?field_id=1"
```

### 3. Obtenir recommandations irrigation

```bash
curl "http://localhost:8000/api/predictions/irrigation?field_id=1"
```

---

## 📈 Modèles ML

### 1. Prédiction Pluie
- **Algorithme :** Prophet + XGBoost
- **Features :** Température, humidité, pression, historique pluie
- **Métrique :** RMSE, MAE
- **Performance :** [À compléter après entraînement]

### 2. Détection Sécheresse
- **Algorithme :** Random Forest
- **Features :** Index végétation, humidité sol, température
- **Métrique :** F1-Score, Precision, Recall
- **Performance :** [À compléter après entraînement]

### 3. Risques Maladies
- **Algorithme :** Règles métier + Classification
- **Features :** Température, humidité, type culture
- **Métrique :** Accuracy, Confusion Matrix
- **Performance :** [À compléter après entraînement]

---

## 🎥 Démo

[Lien vers vidéo démo - À ajouter]

Captures d'écran dans `/docs/screenshots/`

---

## 🤝 Contribution

### Workflow Git

1. Créer une branche feature
```bash
git checkout -b feature/nom-feature
```

2. Commit changements
```bash
git add .
git commit -m "Description du changement"
```

3. Push et créer Pull Request
```bash
git push origin feature/nom-feature
```

---

## 📝 Livrables

- [x] Code source complet
- [x] README.md détaillé
- [x] Captures d'écran (/docs)
- [x] CVs équipe (/team)
- [x] Quiz LMS (/lms)
- [x] Présentation finale (/presentation)

---

## 📄 License

MIT License - Hack2Hire 2024

---

## 📧 Contact

- **Développeur :** Yvan NGOUANA
- **Email :** [Votre email]
- **GitHub :** [https://github.com/yvan-ngouana]
- **LinkedIn :** [Votre profil LinkedIn]

---

## 🙏 Remerciements

- DataBeez pour l'accompagnement
- Hack2Hire pour l'opportunité
- OpenWeather, FAO, Copernicus pour les APIs

---

**Développé avec ❤️ pour l'agriculture africaine**
