"""
Module de notifications SMS/WhatsApp via Twilio
Permet d'envoyer des alertes météo aux agriculteurs
"""

import os
from typing import Optional
from twilio.rest import Client
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


class NotificationService:
    """Service d'envoi de notifications SMS et WhatsApp"""

    def __init__(self):
        """Initialise le client Twilio"""
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.phone_number = os.getenv("TWILIO_PHONE_NUMBER")
        self.whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

        # Mode demo si pas de credentials Twilio
        self.demo_mode = not (self.account_sid and self.auth_token)

        if not self.demo_mode:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                logger.info("Client Twilio initialisé avec succès")
            except Exception as e:
                logger.warning(f"Erreur initialisation Twilio: {e}. Mode démo activé.")
                self.demo_mode = True
        else:
            logger.info("Mode démo activé - notifications simulées")

    def send_sms(self, to_phone: str, message: str) -> dict:
        """
        Envoie un SMS via Twilio

        Args:
            to_phone: Numéro de téléphone destinataire (format: +221XXXXXXXXX)
            message: Message à envoyer

        Returns:
            Dict avec statut d'envoi
        """
        if self.demo_mode:
            logger.info(f"[DEMO SMS] À: {to_phone}")
            logger.info(f"[DEMO SMS] Message: {message}")
            return {
                "success": True,
                "mode": "demo",
                "sid": "demo_sms_" + str(hash(message))[:8],
                "to": to_phone,
                "message": message
            }

        try:
            sms_message = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_phone
            )

            logger.info(f"SMS envoyé avec succès: {sms_message.sid}")

            return {
                "success": True,
                "mode": "real",
                "sid": sms_message.sid,
                "status": sms_message.status,
                "to": to_phone
            }

        except Exception as e:
            logger.error(f"Erreur envoi SMS: {e}")
            return {
                "success": False,
                "error": str(e),
                "to": to_phone
            }

    def send_whatsapp(self, to_phone: str, message: str) -> dict:
        """
        Envoie un message WhatsApp via Twilio

        Args:
            to_phone: Numéro WhatsApp (format: +221XXXXXXXXX)
            message: Message à envoyer

        Returns:
            Dict avec statut d'envoi
        """
        if self.demo_mode:
            logger.info(f"[DEMO WhatsApp] À: {to_phone}")
            logger.info(f"[DEMO WhatsApp] Message: {message}")
            return {
                "success": True,
                "mode": "demo",
                "sid": "demo_whatsapp_" + str(hash(message))[:8],
                "to": to_phone,
                "message": message
            }

        try:
            # Format WhatsApp
            whatsapp_to = f"whatsapp:{to_phone}"
            whatsapp_from = self.whatsapp_number or f"whatsapp:{self.phone_number}"

            whatsapp_message = self.client.messages.create(
                body=message,
                from_=whatsapp_from,
                to=whatsapp_to
            )

            logger.info(f"WhatsApp envoyé avec succès: {whatsapp_message.sid}")

            return {
                "success": True,
                "mode": "real",
                "sid": whatsapp_message.sid,
                "status": whatsapp_message.status,
                "to": to_phone
            }

        except Exception as e:
            logger.error(f"Erreur envoi WhatsApp: {e}")
            return {
                "success": False,
                "error": str(e),
                "to": to_phone
            }

    def send_weather_alert(
        self,
        to_phone: str,
        field_name: str,
        alert_type: str,
        details: dict,
        channel: str = "sms"
    ) -> dict:
        """
        Envoie une alerte météo formatée

        Args:
            to_phone: Numéro destinataire
            field_name: Nom du champ agricole
            alert_type: Type d'alerte (rain, drought, disease, irrigation)
            details: Détails de l'alerte
            channel: "sms" ou "whatsapp"

        Returns:
            Résultat d'envoi
        """
        # Construire le message selon le type
        if alert_type == "rain":
            date_str = details.get('date', "Aujourd'hui")
            message = f"🌧️ Alerte Météo - {field_name}\n"
            message += f"Pluie prévue: {details.get('rain_mm', 0):.1f}mm\n"
            message += f"Date: {date_str}\n"
            message += "→ Pas besoin d'arroser\n"

        elif alert_type == "irrigation":
            date_str = details.get('date', "Aujourd'hui")
            message = f"💧 Recommandation Irrigation - {field_name}\n"
            message += f"Besoin en eau: {details.get('water_amount_mm', 0):.1f}mm\n"
            message += f"Date: {date_str}\n"
            message += f"→ {details.get('reason', 'Irrigation recommandée')}\n"

        elif alert_type == "disease":
            message = f"⚠️ Alerte Maladies - {field_name}\n"
            message += f"Risque: {details.get('risk_level', 'moyen').upper()}\n"
            message += f"Humidité: {details.get('humidity', 0)}%\n"
            message += f"Température: {details.get('temperature', 0):.1f}°C\n"
            message += "→ Surveiller vos cultures\n"

        elif alert_type == "drought":
            message = f"🌵 Alerte Sécheresse - {field_name}\n"
            message += f"Niveau: {details.get('drought_level', 'modéré').upper()}\n"
            message += f"Probabilité: {details.get('probability', 0):.0%}\n"
            message += "→ Planifier irrigation urgente\n"

        else:
            message = f"📱 Alerte - {field_name}\n"
            message += f"Type: {alert_type}\n"
            message += f"Détails: {details}\n"

        # Ajouter footer
        message += "\n📊 Plateforme Météo Agricole"

        # Envoyer selon le canal
        if channel.lower() == "whatsapp":
            return self.send_whatsapp(to_phone, message)
        else:
            return self.send_sms(to_phone, message)

    def send_daily_summary(
        self,
        to_phone: str,
        field_name: str,
        weather_summary: dict,
        channel: str = "sms"
    ) -> dict:
        """
        Envoie un résumé quotidien de la météo

        Args:
            to_phone: Numéro destinataire
            field_name: Nom du champ
            weather_summary: Résumé météo
            channel: "sms" ou "whatsapp"

        Returns:
            Résultat d'envoi
        """
        message = f"📅 Résumé Quotidien - {field_name}\n\n"
        message += f"🌡️ Température: {weather_summary.get('temp_min', 0):.0f}-{weather_summary.get('temp_max', 0):.0f}°C\n"
        message += f"💧 Humidité: {weather_summary.get('humidity', 0)}%\n"
        message += f"🌧️ Pluie: {weather_summary.get('rain_mm', 0):.1f}mm\n"

        if weather_summary.get('irrigation_needed'):
            message += f"\n💦 Irrigation: {weather_summary.get('irrigation_mm', 0):.1f}mm recommandés\n"

        if weather_summary.get('disease_risk', 'low') != 'low':
            message += f"\n⚠️ Risque maladie: {weather_summary.get('disease_risk', 'low').upper()}\n"

        message += "\n📊 Plateforme Météo Agricole"

        if channel.lower() == "whatsapp":
            return self.send_whatsapp(to_phone, message)
        else:
            return self.send_sms(to_phone, message)


# Instance globale pour réutilisation
notification_service = NotificationService()


# Fonctions helper
def send_rain_alert(to_phone: str, field_name: str, rain_mm: float, date: str, channel: str = "sms"):
    """Envoie une alerte pluie"""
    return notification_service.send_weather_alert(
        to_phone=to_phone,
        field_name=field_name,
        alert_type="rain",
        details={"rain_mm": rain_mm, "date": date},
        channel=channel
    )


def send_irrigation_alert(
    to_phone: str,
    field_name: str,
    water_amount_mm: float,
    reason: str,
    date: str,
    channel: str = "sms"
):
    """Envoie une recommandation d'irrigation"""
    return notification_service.send_weather_alert(
        to_phone=to_phone,
        field_name=field_name,
        alert_type="irrigation",
        details={
            "water_amount_mm": water_amount_mm,
            "reason": reason,
            "date": date
        },
        channel=channel
    )


def send_disease_alert(
    to_phone: str,
    field_name: str,
    risk_level: str,
    humidity: float,
    temperature: float,
    channel: str = "sms"
):
    """Envoie une alerte maladie"""
    return notification_service.send_weather_alert(
        to_phone=to_phone,
        field_name=field_name,
        alert_type="disease",
        details={
            "risk_level": risk_level,
            "humidity": humidity,
            "temperature": temperature
        },
        channel=channel
    )


if __name__ == "__main__":
    # Test du service
    service = NotificationService()

    # Test SMS
    result = service.send_sms(
        to_phone="+221771234567",
        message="Test d'alerte météo agricole"
    )
    print("Résultat SMS:", result)

    # Test alerte irrigation
    result = service.send_weather_alert(
        to_phone="+221771234567",
        field_name="Champ Nord",
        alert_type="irrigation",
        details={
            "water_amount_mm": 15.5,
            "date": "2025-11-10",
            "reason": "Faible pluie prévue"
        },
        channel="sms"
    )
    print("Résultat alerte:", result)
