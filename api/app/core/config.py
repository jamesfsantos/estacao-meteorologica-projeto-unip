import os

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "projeto-unip/estacao-meteorologica/temperatura"

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://dashboard.coredevelopement.top",
]