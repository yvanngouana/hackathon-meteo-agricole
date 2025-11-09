# 🚀 Démarrage Rapide - Premiers Pas

## Pour Commencer MAINTENANT (30 minutes)

### Étape 1 : Configuration Git (5 min)

```bash
# Configurer votre identité Git
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"

# Vérifier
git config --list

# Créer premier commit
git add -A
git commit -m "feat: Initial project setup - Hack2Hire"

# Créer branche dev
git checkout -b dev
```

### Étape 2 : Obtenir Clés API (10 min)

#### OpenWeather API (OBLIGATOIRE)
1. Aller sur : https://openweathermap.org/api
2. Créer compte gratuit
3. Générer clé API (section "API keys")
4. Copier la clé

#### Twilio (OPTIONNEL - pour SMS)
1. Aller sur : https://www.twilio.com/try-twilio
2. Créer compte trial gratuit
3. Obtenir Account SID + Auth Token
4. Numéro de téléphone test fourni

### Étape 3 : Configuration Environnement (10 min)

```bash
# Copier le template
cp .env.example .env

# Éditer .env
nano .env  # ou code .env, vim .env, etc.
```

**Remplacer au minimum :**
```env
OPENWEATHER_API_KEY=votre_cle_openweather_ici
```

**Optionnel (SMS) :**
```env
TWILIO_ACCOUNT_SID=votre_sid
TWILIO_AUTH_TOKEN=votre_token
TWILIO_PHONE_NUMBER=+1234567890
```

### Étape 4 : Premier Test (5 min)

#### Option A : Avec Docker (RECOMMANDÉ)

```bash
# Démarrer seulement PostgreSQL et API
docker-compose up -d postgres api

# Attendre 10 secondes que PostgreSQL démarre
sleep 10

# Tester l'API
curl http://localhost:8000/health
```

#### Option B : Sans Docker (Python local)

```bash
# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou : venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt

# Lancer API
cd src
uvicorn api.main:app --reload
```

### Étape 5 : Tester Météo (immédiat)

```bash
# Météo Dakar
curl "http://localhost:8000/api/weather/current?latitude=14.7167&longitude=-17.4677"

# Prévisions 7 jours
curl "http://localhost:8000/api/weather/forecast?latitude=14.7167&longitude=-17.4677&days=7"
```

---

## 📋 Checklist Jour 1

### Membre 1 (Data Engineer)
```bash
# Vérifier Docker fonctionne
docker --version
docker-compose --version

# Lancer PostgreSQL
docker-compose up -d postgres

# Tester connexion
docker-compose exec postgres psql -U postgres -d meteo_agricole -c "SELECT version();"

# Créer tables
cd src
python -c "from etl.load import DatabaseLoader; DatabaseLoader()"
```

### Membre 2 (Data Scientist)
```bash
# Setup Jupyter
pip install jupyter notebook
jupyter notebook

# Créer premier notebook
# notebooks/01_data_exploration.ipynb

# Tester extraction données
cd src
python -c "from etl.extract import WeatherDataExtractor; w = WeatherDataExtractor(); print(w.get_current_weather(14.7167, -17.4677))"
```

### Membre 3 (Full Stack)
```bash
# Tester API
curl http://localhost:8000
curl http://localhost:8000/docs  # Ouvrir dans navigateur

# Tester endpoints
curl http://localhost:8000/health

# Setup frontend (si temps)
cd src/frontend
npx create-react-app . --template typescript
npm install plotly.js react-plotly.js axios
```

---

## 🎯 Objectifs Fin Jour 1

- [ ] Git configuré et premier commit
- [ ] Clés API obtenues
- [ ] .env configuré
- [ ] Docker/Python fonctionne
- [ ] API répond (health check)
- [ ] PostgreSQL connecté
- [ ] Extraction météo testée
- [ ] Équipe synchronisée

---

## 🆘 Aide Rapide

### Problème : "command not found: docker"
```bash
# Installer Docker
# Linux Ubuntu/Debian :
sudo apt update
sudo apt install docker.io docker-compose

# Mac :
brew install docker docker-compose
```

### Problème : "Port 8000 already in use"
```bash
# Changer port dans docker-compose.yml
# Ligne ports: "8001:8000" au lieu de "8000:8000"
```

### Problème : "Module not found: requests"
```bash
# Vérifier venv activé
which python  # Doit montrer path venv

# Réinstaller
pip install -r requirements.txt
```

### Problème : "API returns 500 error"
```bash
# Voir logs
docker-compose logs api

# Vérifier .env
cat .env | grep OPENWEATHER_API_KEY
```

---

## 📚 Ressources Utiles

### Documentation Externe
- OpenWeather API : https://openweathermap.org/api/one-call-3
- FastAPI Docs : https://fastapi.tiangolo.com
- Airflow Docs : https://airflow.apache.org/docs
- Docker Compose : https://docs.docker.com/compose

### Documentation Interne
- [README complet](README.md)
- [Architecture](docs/architecture.md)
- [Quickstart détaillé](docs/QUICKSTART.md)
- [Plan 10 jours](PLAN_EXECUTION_10_JOURS.md)
- [Contributing](CONTRIBUTING.md)

### Commandes Fréquentes
```bash
# Docker
docker-compose up -d          # Démarrer services
docker-compose ps             # État services
docker-compose logs api       # Logs API
docker-compose down           # Arrêter services
docker-compose restart api    # Redémarrer API

# Git
git status                    # État repo
git add .                     # Ajouter fichiers
git commit -m "message"       # Commit
git push origin dev           # Push branche

# Python
source venv/bin/activate      # Activer venv
pip list                      # Packages installés
pytest tests/ -v              # Lancer tests
black src/                    # Formater code
```

---

## 💡 Conseils Équipe

### Communication
- **Slack/Discord** : Chat quotidien
- **GitHub Issues** : Tracker bugs/features
- **Daily Standup** : 9h00 (15 min)

### Organisation
- Chacun sur sa branche feature
- Merge sur dev régulièrement
- Merge dev → main pour livrables

### Productivité
- Commit fréquents (toutes les 1-2h)
- Code review mutuel
- Ne pas bloquer sur un problème > 30 min (demander aide)
- Focus MVP avant optimisations

---

## 🎉 Vous êtes prêts !

Suivez le **PLAN_EXECUTION_10_JOURS.md** pour le détail jour par jour.

**Prochain step** : Chaque membre commence ses tâches Jour 1 !

Bon courage ! 💪🚀
