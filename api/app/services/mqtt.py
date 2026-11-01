import json
import paho.mqtt.client as mqtt
from app.core.config import MQTT_TOPIC
from app.database.connection import ContextoBanco
from app.database.models import Medidas, Localizacao
from app.schemas.medidas import PayloadEsp32
from datetime import datetime
dados_estacao = PayloadEsp32()

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Conectado ao Broker MQTT! Código: {reason_code}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global dados_estacao
    try:
        payload = msg.payload.decode("utf-8")
        dados_json = json.loads(payload)
        dados_estacao = PayloadEsp32.model_validate(dados_json)

        print(f"Dados recebidos via MQTT: {dados_estacao}")

        

        with ContextoBanco() as db:
            
            #Verificando se a localização já existe...
            
            loc = db.query(Localizacao).where(
                Localizacao.latitude == dados_estacao.latitude, 
                Localizacao.longitude == dados_estacao.longitude
            ).first()
            
            localizacao_id = None
            
            if not loc:
                localizacao = Localizacao(
                    latitude=dados_estacao.latitude,
                    longitude=dados_estacao.longitude,
                    precisao=dados_estacao.precisao
                )
                
                db.add(localizacao)
                db.flush()
                localizacao_id = localizacao.id
            else:
                localizacao_id = loc.id
                
                
            print(f"ID localização: {localizacao_id}")
            
            
            medida = Medidas(
                temperatura=dados_estacao.temperatura,
                umidade=dados_estacao.umidade,
                pressao=dados_estacao.pressao,
                temperatura_bmp=dados_estacao.temperatura_bmp,
                luminosidade=dados_estacao.luminosidade,
                gas=dados_estacao.gas,
                gas_digital=dados_estacao.gas_digital,
                id_localizacao=localizacao_id,
                data_cadastro=datetime.now()
            )
            
            db.add(medida)
            db.commit()
            
            print(f"""
Latitude: {dados_estacao.latitude}
Longitude: {dados_estacao.longitude}
Precisão: {dados_estacao.precisao}
                  """)
            
            print(f"""
Temperatura: {dados_estacao.temperatura}°c
Umidade: {dados_estacao.umidade}% UR
Pressão: {dados_estacao.pressao}kPa
Luminosidade: {dados_estacao.luminosidade}lx
Gás: {dados_estacao.gas}%
                """)
            

    except Exception as e:
        print(f"Erro ao processar mensagem MQTT: {e}")

def setup_mqtt() -> mqtt.Client:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    return client