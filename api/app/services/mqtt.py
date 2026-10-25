import json
import paho.mqtt.client as mqtt
from core.config import MQTT_TOPIC
from database.connection import ContextoBanco
from database.models import Medidas
from schemas import DadosTemperatura

dados_estacao = DadosTemperatura()

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Conectado ao Broker MQTT! Código: {reason_code}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global dados_estacao
    try:
        payload = msg.payload.decode("utf-8")
        dados_json = json.loads(payload)
        dados_estacao = DadosTemperatura.model_validate(dados_json)

        print(f"Dados recebidos via MQTT: {dados_estacao}")

        with ContextoBanco() as db:
            medida = Medidas(
                temperatura=dados_estacao.temperatura,
                umidade=dados_estacao.umidade,
                pressao=dados_estacao.pressao,
                temperatura_bmp=dados_estacao.temperatura_bmp,
                luminosidade=dados_estacao.luminosidade,
                gas=dados_estacao.gas,
                gas_digital=dados_estacao.gas_digital,
            )
            db.add(medida)
            db.commit()
            print(f"""
                Temperatura: {dados_estacao.temperatura}°c
                Umidade: {dados_estacao.umidade}% UR
                Pressão: {dados_estacao.pressao}kPa
                Luminosidade: {dados_estacao.luminosidade}lx
                Gás: {dados_estacao.gas}%
            """)
            print("Medida registrada.")

    except Exception as e:
        print(f"Erro ao processar mensagem MQTT: {e}")

def setup_mqtt() -> mqtt.Client:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    return client