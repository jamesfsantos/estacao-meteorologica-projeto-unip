from contextlib import asynccontextmanager
import json
from fastapi import FastAPI
from pydantic import BaseModel
import paho.mqtt.client as mqtt


class DadosTemperatura(BaseModel):
    temperatura: str = "0.0"
    umidade: str = "0.0"
    pressao: str = "0"
    temperatura_bmp: str = "0.0"
    luminosidade: str = "0"
    gas: str = "0"
    gas_digital: str = "0"

dados_estacao = DadosTemperatura()

# 2. Configuração dos Callbacks MQTT
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Conectado ao Broker MQTT! Código: {reason_code}")
    
    # Aqui lê onde vai pegar as mensagens.
    client.subscribe("projeto-unip/estacao-meteorologica/temperatura")

def on_message(client, userdata, msg):
    global dados_estacao #Modica 
    try:
        payload = msg.payload.decode("utf-8")
        dados_json = json.loads(payload)
        
        
        dados_estacao = DadosTemperatura.model_validate(dados_json)
        print(f"Dados atualizados via MQTT: {dados_estacao}")
    except Exception as e:
        print(f"Erro ao processar mensagem MQTT: {e}")


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message


@asynccontextmanager
async def lifespan(app: FastAPI):
    mqttc.connect("broker.hivemq.com", 1883, 60)
    mqttc.loop_start()
    yield # Esse é o responsavel por detectar quando encerra a aplicação: CTRL + C..
    mqttc.loop_stop()
    mqttc.disconnect()


app = FastAPI(lifespan=lifespan)

# 6. Endpoints
@app.get("/")
def read_root():
    return dados_estacao