# 🌾 Plateforme d'Intelligence Météo & Agricole

## Hack2Hire - Édition 2

**Développeur :** Yvan NGOUANA
**Email :** yvan.ngouana@yahoo.com          
**Téléphone :** +237 693 451 088   

**Data Engineer & Data Analyst:** Serigne Babacar KANE
**Email:** bgserignebabacar@gmail.com
**Téléphone:** +221781575821

---

## 📋 Description du Projet

Plateforme intelligente d'aide à la décision agricole pour les agriculteurs du Sénégal, combinant :

- **Prévisions météorologiques** adaptées aux coordonnées GPS des champs
- **Recommandations d'irrigation** basées sur les conditions météo
- **Alertes maladies** en fonction de l'humidité et de la température
- **Interface web intuitive** avec visualisations graphiques
- **Notifications SMS/WhatsApp** via Twilio

**Objectif :** Aider les agriculteurs à optimiser leurs décisions de semis, d'irrigation et de récolte pour améliorer les rendements et réduire les pertes.

---

## 🏗️ Architecture Technique

### Stack Technologique

**Backend & Data**
- **Python 3.10+** - Langage principal
- **FastAPI** - API REST moderne et performante
- **Apache Airflow** - Orchestration des pipelines ETL
- **PostgreSQL + TimescaleDB** - Base de données temporelles (optionnel)
- **Docker & Docker Compose** - Conteneurisation

**Machine Learning**
- **scikit-learn** - Modèles de classification
- **XGBoost** - Gradient boosting
- **Prophet** - Prévisions séries temporelles
- **Pandas, NumPy** - Manipulation de données

**Frontend**
- **React 18.2** - Framework JavaScript
- **React Bootstrap 5.2** - Composants UI
- **Plotly.js** - Visualisations interactives
- **React Router v6** - Navigation
- **Axios** - Requêtes HTTP

**APIs Externes**
- **OpenWeather One Call 3.0** - Données météo en temps réel
- **Twilio** - Notifications SMS/WhatsApp

**DevOps**
- **Docker** - Conteneurisation
- **GitHub Actions** - CI/CD
- **Nginx** - Reverse proxy (production)

### Architecture Système

```
┌─────────────────────────────────────────────────────┐
│              Sources de Données                     │
│         OpenWeather API (One Call 3.0)              │
└──────────────────┬──────────────────────────────────┘
                   │
         ┌─────────▼─────────┐
         │   ETL Pipeline    │
         │  (Apache Airflow) │
         │  - Extract        │
         │  - Transform      │
         │  - Load           │
         └─────────┬─────────┘
                   │
         ┌─────────▼─────────┐
         │  PostgreSQL +     │
         │  TimescaleDB      │
         │  (Optionnel)      │
         └─────────┬─────────┘
                   │
         ┌─────────▼─────────┐
         │   Modèles ML/AI   │
         │  - Irrigation     │
         │  - Maladies       │
         │  - Prédictions    │
         └─────────┬─────────┘
                   │
         ┌─────────▼─────────┐
         │   API FastAPI     │
         │  /weather         │
         │  /predictions     │
         │  /notifications   │
         └─────────┬─────────┘
                   │
    ┌──────────────┴──────────────┐
    │                             │
┌───▼────────┐          ┌─────────▼─────────┐
│  Frontend  │          │  Notifications    │
│  React +   │          │  SMS/WhatsApp     │
│  Bootstrap │          │  (Twilio)         │
└────────────┘          └───────────────────┘
```

---

## 🚀 Installation & Lancement

### Prérequis

- **Python 3.10+**
- **Node.js 18+** (pour le frontend)
- **Docker & Docker Compose** (optionnel mais recommandé)
- **Git**
- Clé API OpenWeather (gratuite sur [openweathermap.org](https://openweathermap.org))

### Installation Rapide

#### Option 1: Avec Docker (Recommandé)

```bash
# 1. Cloner le repository
git clone <url-du-repo>
cd hackathon

# 2. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env et ajouter votre clé OpenWeather

# 3. Lancer tous les services
docker-compose up -d

# 4. Accéder à l'application
# Frontend: http://localhost:3000
# API: http://localhost:8000/docs
# Airflow: http://localhost:8080 (admin/admin)
```

#### Option 2: Sans Docker (Développement)

```bash
# 1. Cloner le repository
git clone <url-du-repo>
cd hackathon

# 2. Installer dépendances Python
pip install -r requirements.txt

# 3. Configurer variables d'environnement
cp .env.example .env
# Éditer .env

# 4. Lancer l'API (terminal 1)
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# 5. Lancer le frontend (terminal 2)
cd src/frontend
npm install
npm start

# 6. Accéder à l'application
# Frontend: http://localhost:3000
# API: http://localhost:8000/docs
```

---

## 📂 Structure du Projet

```
hackathon/
├── README.md                          # Ce fichier
├── requirements.txt                   # Dépendances Python
├── docker-compose.yml                 # Configuration Docker
├── .env.example                       # Template variables d'environnement
├── .gitignore
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml                  # Pipeline CI/CD
│
├── data/
│   ├── raw/                           # Données brutes
│   ├── processed/                     # Données transformées
│   └── models/                        # Modèles ML entraînés
│
├── src/
│   ├── api/
│   │   ├── main.py                    # Point d'entrée FastAPI
│   │   ├── config.py                  # Configuration
│   │   ├── database.py                # Connexion DB
│   │   └── routers/
│   │       ├── weather.py             # Endpoints météo
│   │       ├── predictions.py         # Endpoints ML
│   │       └── notifications.py       # Endpoints SMS/WhatsApp
│   │
│   ├── etl/
│   │   ├── extract.py                 # Extraction données APIs
│   │   ├── transform.py               # Transformation & nettoyage
│   │   └── load.py                    # Chargement PostgreSQL
│   │
│   ├── models/
│   │   ├── rain_prediction.py         # Modèle prédiction pluie
│   │   ├── irrigation.py              # Recommandations irrigation
│   │   └── disease_risk.py            # Risques maladies
│   │
│   └── frontend/
│       ├── public/
│       ├── src/
│       │   ├── components/
│       │   │   ├── Auth.js            # Authentification
│       │   │   ├── Header.js          # Navigation
│       │   │   └── Footer.js          # Pied de page
│       │   │
│       │   ├── pages/
│       │   │   ├── Dashboard.js       # Tableau de bord
│       │   │   ├── WeatherForecast.js # Prévisions météo
│       │   │   ├── WeatherAlerts.js   # Gestion alertes
│       │   │   ├── IrrigationRecommendations.js
│       │   │   ├── FieldManagement.js # Gestion champs
│       │   │   └── DiseaseAlerts.js   # Alertes maladies
│       │   │
│       │   ├── App.js                 # Composant principal
│       │   ├── App.css                # Styles
│       │   └── index.js               # Point d'entrée
│       │
│       └── package.json
│
├── airflow/
│   └── dags/
│       └── weather_etl_dag.py         # Pipeline ETL automatisé
│
├── tests/
│   ├── test_etl.py                    # Tests ETL
│   ├── test_api.py                    # Tests API
│   └── test_models.py                 # Tests ML
│
├── docs/
│   ├── architecture.md                # Documentation architecture
│   ├── QUICKSTART.md                  # Guide démarrage rapide
│   └── API_DOCUMENTATION.md           # Documentation API
│
├── presentation/
│   ├── PLAN_PRESENTATION.md           # Plan de présentation
│   └── slides_finale.md               # Slides finales
│
└── lms/
    └── README.md                      # Résultats LMS
```

---

## 🎯 Fonctionnalités Implémentées

### ✅ API Backend (FastAPI)

- **Endpoints Météo**
  - `GET /api/weather/current` - Météo actuelle par coordonnées
  - `GET /api/weather/forecast` - Prévisions 3/7/14 jours
  - `GET /health` - Health check

- **Endpoints ML & Prédictions**
  - `GET /api/predictions/irrigation` - Recommandations d'irrigation
  - `GET /api/predictions/disease-risk` - Risques de maladies
  - `POST /api/predictions/rain` - Prédiction pluie

- **Endpoints Notifications**
  - `POST /api/notifications/sms` - Envoyer SMS
  - `POST /api/notifications/whatsapp` - Envoyer WhatsApp
  - `POST /api/notifications/alert` - Alerte personnalisée

### ✅ Interface Web (React)

- **Authentification**
  - Page de connexion
  - Page d'inscription
  - Gestion de session (localStorage)
  - Routes protégées

- **Tableau de Bord**
  - Cartes météo en temps réel (Température, Humidité, Vent)
  - Graphique température (7 jours)
  - Graphique précipitations (7 jours)
  - Indicateurs agricoles

- **Prévisions Météo**
  - Recherche par coordonnées GPS
  - Sélection période (3/7/14 jours)
  - 3 graphiques interactifs (Plotly)
  - Résumé des conditions

- **Gestion des Champs**
  - Ajout de champs agricoles
  - Liste des champs avec coordonnées
  - Type de culture
  - Superficie en hectares

- **Alertes Météo**
  - Configuration d'alertes personnalisées
  - Conditions de déclenchement (temp, pluie, humidité)
  - Fréquence (horaire, quotidien, hebdomadaire)
  - Activation/Désactivation

- **Recommandations d'Irrigation**
  - Graphique besoins en eau
  - Table détaillée par jour
  - Calcul total eau nécessaire
  - Raisons des recommandations

- **Alertes Maladies**
  - Niveaux de risque (Faible/Modéré/Élevé)
  - Facteurs environnementaux
  - Recommandations par niveau
  - Code couleur visuel

### ✅ Pipeline ETL (Airflow)

- Extraction données OpenWeather API
- Transformation et nettoyage
- Stockage TimescaleDB (optionnel)
- Exécution automatisée (scheduling)

### ✅ DevOps

- Conteneurisation complète (Docker)
- Docker Compose multi-services
- CI/CD GitHub Actions
- Déploiement production avec Nginx

---

## 🔧 Configuration

### Variables d'Environnement (.env)

```env
# OpenWeather API
OPENWEATHER_API_KEY=1e0774d9014214237bcbfe77950f3f51

# Mode démonstration (utilise données de démo si API indisponible)
USE_MOCK_DATA=True

# Database (optionnel)
DATABASE_URL=postgresql://user:password@localhost:5432/meteo_agricole

# Twilio (pour notifications SMS/WhatsApp)
TWILIO_ACCOUNT_SID=your_sid_here
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890

# Application
APP_ENV=development
SECRET_KEY=your_secret_key_here
DEBUG=True
```

---

## 📊 Utilisation de l'API

### 1. Obtenir la météo actuelle

```bash
curl "http://localhost:8000/api/weather/current?latitude=14.7167&longitude=-17.4677"
```

**Réponse:**
```json
{
  "location": {
    "latitude": 14.7167,
    "longitude": -17.4677
  },
  "weather": {
    "temperature_celsius": 28.5,
    "humidity_percent": 65,
    "wind_speed_ms": 4.2,
    "weather_description": "Ciel dégagé"
  }
}
```

### 2. Obtenir les prévisions

```bash
curl "http://localhost:8000/api/weather/forecast?latitude=14.7167&longitude=-17.4677&days=7"
```

### 3. Recommandations d'irrigation

```bash
curl "http://localhost:8000/api/predictions/irrigation?latitude=14.7167&longitude=-17.4677&days=7"
```

**Réponse:**
```json
{
  "recommendations": [
    {
      "date": "2024-01-15",
      "irrigation_needed": true,
      "water_amount_mm": 5.2,
      "reason": "Faible probabilité de pluie"
    }
  ]
}
```

### 4. Envoyer notification SMS

```bash
curl -X POST "http://localhost:8000/api/notifications/sms" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+221701234567",
    "message": "Alerte météo: Risque de sécheresse dans 3 jours"
  }'
```

---

## 🧪 Tests

```bash
# Lancer tous les tests
pytest tests/ -v

# Tests avec couverture
pytest --cov=src tests/

# Tests API uniquement
pytest tests/test_api.py -v

# Tests ETL
pytest tests/test_etl.py -v
```

---

## 📈 Modèles Machine Learning

### 1. Recommandations d'Irrigation

**Approche:** Règles métier + Machine Learning

**Logique:**
- Analyse de la probabilité de pluie
- Évapotranspiration estimée
- Type de culture
- Humidité du sol (si capteurs IoT)

**Sortie:** Quantité d'eau nécessaire (mm) par jour

### 2. Détection Risques Maladies

**Approche:** Classification basée sur conditions météo

**Features:**
- Humidité relative (%)
- Température (°C)
- Précipitations récentes
- Type de culture

**Niveaux de risque:**
- Faible: Humidité < 60% ou Temp < 15°C
- Modéré: 60% < Humidité < 75%
- Élevé: Humidité > 75% ET 15°C < Temp < 30°C

**Recommandations:**
- Risque faible: Surveillance normale
- Risque modéré: Inspection régulière
- Risque élevé: Application fongicides préventifs

### 3. Prédiction Pluie

**Algorithme:** XGBoost + Prophet

**Features:**
- Données historiques météo
- Pression atmosphérique
- Température
- Humidité
- Vent

**Métrique:** RMSE, MAE

---

## 🎨 Captures d'Écran

### Tableau de Bord
![Dashboard](docs/screenshots/dashboard.png)

### Prévisions Météo
![Forecasts](docs/screenshots/forecasts.png)

### Recommandations Irrigation
![Irrigation](docs/screenshots/irrigation.png)

---

## 🚀 Déploiement Production

### Avec Docker Compose

```bash
# 1. Configurer variables production
cp .env.example .env.production
nano .env.production

# 2. Lancer en mode production
docker-compose -f docker-compose.production.yml up -d

# 3. Vérifier statut
docker-compose -f docker-compose.production.yml ps

# 4. Voir logs
docker-compose -f docker-compose.production.yml logs -f
```

### Sur Serveur (VPS/Cloud)

**Prérequis:** Serveur Ubuntu 20.04+ avec Docker installé

```bash
# 1. Sur le serveur
git clone <url-du-repo>
cd hackathon

# 2. Configuration
cp .env.example .env
nano .env  # Éditer avec vraies valeurs

# 3. Lancer
./deploy.sh prod

# 4. Nginx reverse proxy (optionnel)
sudo apt install nginx
sudo cp nginx/conf.d/meteo.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/meteo.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**Application accessible sur:** `http://votre-serveur.com`

---

## 📝 Documentation Complète

- [Architecture Détaillée](docs/architecture.md)
- [Documentation API](docs/API_DOCUMENTATION.md)
- [Guide Démarrage Rapide](docs/QUICKSTART.md)
- [Guide Déploiement](docs/development/GUIDE_DEPLOIEMENT.md)

---

## 🎥 Vidéo Démo

[Lien vers vidéo YouTube - À ajouter]

---

## 🏆 Livrables Hack2Hire

- ✅ **Code source complet** - Repository GitHub
- ✅ **Application fonctionnelle** - API + Frontend + ETL
- ✅ **Documentation technique** - README + docs/
- ✅ **Tests automatisés** - tests/
- ✅ **Conteneurisation** - Docker + Docker Compose
- ✅ **Présentation** - presentation/slides_finale.md
- ✅ **Quiz LMS** - lms/

---

## 🔮 Évolutions Futures

- [ ] Application mobile (React Native)
- [ ] Intégration capteurs IoT
- [ ] Modèles ML plus avancés (Deep Learning)
- [ ] Support multi-pays (Afrique de l'Ouest)
- [ ] API GraphQL
- [ ] Interface multilingue (Wolof, Français, Anglais)
- [ ] Chatbot agricole avec IA
- [ ] Marketplace de produits agricoles

---

## 🛠️ Technologies Utilisées

| Catégorie | Technologies |
|-----------|-------------|
| **Backend** | FastAPI, Python 3.10, SQLAlchemy, Pydantic |
| **Frontend** | React 18.2, React Bootstrap 5.2, Plotly.js, React Router v6 |
| **Data Engineering** | Apache Airflow, Pandas, NumPy |
| **Machine Learning** | scikit-learn, XGBoost, Prophet |
| **Base de Données** | PostgreSQL, TimescaleDB |
| **DevOps** | Docker, Docker Compose, GitHub Actions, Nginx |
| **APIs** | OpenWeather, Twilio |
| **Tests** | Pytest |

---

## 📄 Licence

MIT License - Copyright (c) 2024 Yvan NGOUANA

---

## 📧 Contact

**Yvan NGOUANA**
 Email: contact@meteo-agricole.sn
 Téléphone: +237 693 451 088
 GitHub: github.com/yvanngouana
 LinkedIn: linkedin.com/in/yvan.ngouana

 **Serigne Babacar KANE**
 Email: bgserignebabacar@gmail.com
 Téléphone: +221 781575821
 GitHub: https://github.com/Goorgui-5
 LinkedIn: www.linkedin.com/in/serigne-babacar-kane-6b9759206

---

## 🙏 Remerciements

- **DataBeez** - Pour l'accompagnement et la formation
- **Hack2Hire Édition 2** - Pour l'opportunité
- **OpenWeather** - Pour l'accès à l'API météo
- **Twilio** - Pour les services de messagerie
- **Communauté Open Source** - Pour les outils exceptionnels

---

**🌾 Développé avec passion pour l'agriculture africaine 🚜**

*Un agriculteur informé est un agriculteur prospère*

