#!/usr/bin/env python3
"""
Test direct de l'API OpenWeather avec la vraie clé
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

# Import de l'extracteur
from src.etl.extract import WeatherDataExtractor

def test_real_weather():
    """Test avec vraies données OpenWeather"""
    print("🌍 TEST API OPENWEATHER - VRAIES DONNÉES")
    print("=" * 60)

    extractor = WeatherDataExtractor()

    # Coordonnées de Dakar, Sénégal
    latitude = 14.7167
    longitude = -17.4677

    print(f"\n📍 Localisation: Dakar, Sénégal")
    print(f"   Latitude: {latitude}")
    print(f"   Longitude: {longitude}")
    print(f"\n⚙️  Mode MOCK: {extractor.use_mock}")
    print(f"🔑 Clé API: {extractor.api_key[:10]}..." if extractor.api_key else "❌ Pas de clé API")

    try:
        # Test météo actuelle
        print("\n\n1️⃣  TEST: Météo Actuelle")
        print("-" * 60)
        current = extractor.get_current_weather(latitude, longitude)

        print(f"✅ Succès ! Données reçues:")
        print(f"   🌡️  Température: {current.get('main', {}).get('temp', 'N/A')}°C")
        print(f"   💧 Humidité: {current.get('main', {}).get('humidity', 'N/A')}%")
        print(f"   ☁️  Conditions: {current.get('weather', [{}])[0].get('description', 'N/A')}")
        print(f"   🌬️  Vent: {current.get('wind', {}).get('speed', 'N/A')} m/s")

        # Test prévisions
        print("\n\n2️⃣  TEST: Prévisions 3 Jours")
        print("-" * 60)
        forecast = extractor.get_forecast(latitude, longitude, days=3)

        print(f"✅ Succès ! {len(forecast)} prévisions reçues:")
        for i, day_forecast in enumerate(forecast[:3], 1):
            temp_day = day_forecast.get('temp', {}).get('day', 'N/A')
            humidity = day_forecast.get('humidity', 'N/A')
            rain = day_forecast.get('rain', 0)
            print(f"   Jour {i}: 🌡️ {temp_day}°C | 💧 {humidity}% | 🌧️ {rain}mm")

        print("\n" + "=" * 60)
        print("✅ TOUTES LES DONNÉES MÉTÉO RÉELLES FONCTIONNENT !")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_real_weather()
    sys.exit(0 if success else 1)
