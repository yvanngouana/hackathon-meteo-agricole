# Documentation API - Plateforme Météo Agricole

## =€ Démarrage Rapide

**Base URL:** `http://localhost:8000`

**Documentation Interactive:** `http://localhost:8000/docs` (Swagger UI)

---

## =á Endpoints Disponibles

### 1. Health Check

**GET** `/health`

Vérifie que l'API est opérationnelle.

**Exemple:**
```bash
curl http://localhost:8000/health
```

**Réponse:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-09T03:56:37.133308"
}
```

---

### 2. Météo Actuelle

**GET** `/api/weather/current`

Récupère les conditions météo actuelles pour une localisation.

**Paramètres:**
- `latitude` (float, required): Latitude du champ
- `longitude` (float, required): Longitude du champ

**Exemple:**
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
    "timestamp": "2025-11-09T03:56:37",
    "temperature_celsius": 28.5,
    "feels_like_celsius": 30.2,
    "humidity_percent": 75,
    "pressure_hpa": 1013,
    "wind_speed_ms": 4.2,
    "clouds_percent": 40,
    "uvi": 8.5,
    "weather_description": "partly cloudy"
  }
}
```

---

### 3. Prévisions Météo

**GET** `/api/weather/forecast`

Récupère les prévisions météo pour les prochains jours.

**Paramètres:**
- `latitude` (float, required): Latitude du champ
- `longitude` (float, required): Longitude du champ
- `days` (int, optional, default=7): Nombre de jours de prévision (1-7)

**Exemple:**
```bash
curl "http://localhost:8000/api/weather/forecast?latitude=14.7167&longitude=-17.4677&days=7"
```

**Réponse:**
```json
{
  "location": {
    "latitude": 14.7167,
    "longitude": -17.4677
  },
  "forecasts": [
    {
      "date": "2025-11-09",
      "temp_min": 22.5,
      "temp_max": 32.1,
      "temp_day": 28.0,
      "humidity": 70,
      "rain_mm": 5.2,
      "pop": 65,
      "et0_mm": 4.8,
      "irrigation_need_mm": 0,
      "disease_risk": "medium"
    }
  ],
  "count": 7
}
```

---

### 4. Recommandations d'Irrigation

**GET** `/api/predictions/irrigation`

Obtient les recommandations d'irrigation basées sur les prévisions météo et l'évapotranspiration.

**Paramètres:**
- `latitude` (float, required): Latitude du champ
- `longitude` (float, required): Longitude du champ
- `days` (int, optional, default=7): Période de prévision

**Exemple:**
```bash
curl "http://localhost:8000/api/predictions/irrigation?latitude=14.7167&longitude=-17.4677&days=7"
```

**Réponse:**
```json
{
  "location": {
    "latitude": 14.7167,
    "longitude": -17.4677
  },
  "recommendations": [
    {
      "date": "2025-11-09",
      "irrigation_needed": true,
      "water_amount_mm": 8.5,
      "reason": "Besoin en eau estimé: 8.5mm (ET0 - pluie)"
    },
    {
      "date": "2025-11-10",
      "irrigation_needed": false,
      "water_amount_mm": 0,
      "reason": "Pluie suffisante ou faible évapotranspiration"
    }
  ],
  "period_days": 7
}
```

---

### 5. Risques de Maladies

**GET** `/api/predictions/disease-risk`

Détecte les risques de maladies agricoles basés sur les conditions météo (humidité + température).

**Paramètres:**
- `latitude` (float, required): Latitude du champ
- `longitude` (float, required): Longitude du champ
- `days` (int, optional, default=7): Période de prévision

**Exemple:**
```bash
curl "http://localhost:8000/api/predictions/disease-risk?latitude=14.7167&longitude=-17.4677"
```

**Réponse:**
```json
{
  "location": {
    "latitude": 14.7167,
    "longitude": -17.4677
  },
  "alerts": [
    {
      "date": "2025-11-10",
      "risk_level": "high",
      "humidity": 82,
      "temperature": 26.5,
      "recommendation": "Risque élevé de maladies fongiques. Surveiller les cultures."
    }
  ],
  "alert_count": 1
}
```

---

### 6. Créer un Champ Agricole

**POST** `/api/fields`

Enregistre un nouveau champ agricole dans le système.

**Body (JSON):**
```json
{
  "name": "Champ Nord",
  "latitude": 14.7167,
  "longitude": -17.4677,
  "crop_type": "riz",
  "area_hectares": 2.5
}
```

**Exemple:**
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

**Réponse:**
```json
{
  "id": 1234,
  "message": "Champ créé avec succès (mode démo)",
  "field": {
    "name": "Champ Nord",
    "latitude": 14.7167,
    "longitude": -17.4677,
    "crop_type": "riz",
    "area_hectares": 2.5
  }
}
```

---

## =' Configuration

### Mode MOCK (Développement sans API OpenWeather)

Le mode MOCK est activé par défaut pour permettre le développement sans clé API.

**Dans `.env`:**
```env
USE_MOCK_DATA=True
```

Pour utiliser les vraies données OpenWeather:
```env
USE_MOCK_DATA=False
OPENWEATHER_API_KEY=votre_clé_ici
```

---

## =¨ Codes d'Erreur

| Code | Description |
|------|-------------|
| 200  | Succès |
| 201  | Créé avec succès |
| 400  | Requête invalide |
| 404  | Ressource non trouvée |
| 500  | Erreur serveur |

---

## =Ê Modèles ML Utilisés

### 1. Prédiction Pluie
- **Algorithme:** Random Forest Regressor
- **Features:** temp_day, humidity, pressure, clouds, pop
- **Output:** Quantité de pluie en mm

### 2. Détection Sécheresse
- **Algorithme:** Random Forest Classifier
- **Features:** Cumul pluie 7/30j, ET0, stress hydrique
- **Output:** Niveau de sécheresse (low/medium/high)

### 3. Risque Maladies
- **Algorithme:** Règles métier + Classification
- **Conditions:** Humidité > 70% + Température 15-30°C
- **Output:** Niveau de risque (low/medium/high)

---

## =, Formules Utilisées

### Évapotranspiration (ET0)
Formule simplifiée Hargreaves:
```
ET0 = 0.0023 × (T_mean + 17.8) × (T_amplitude)
```

### Besoin en Irrigation
```
Irrigation_need = max(0, ET0 - Pluie)
```

### Index de Stress Hydrique
```
Water_stress = max(0, (T_max - 25) × (100 - Humidity) / 100)
```

---

## =Ý Notes

- L'API utilise le système métrique (Celsius, mm, km/h)
- Les coordonnées géographiques utilisent le système WGS84
- Les timestamps sont en format ISO 8601
- La documentation interactive complète est disponible sur `/docs`

---

**Développé par:** Yvan NGOUANA
**Hack2Hire Édition 2** - DataBeez
