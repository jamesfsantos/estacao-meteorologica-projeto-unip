from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import ALLOWED_ORIGINS,MQTT_BROKER,MQTT_PORT
from app.database.connection import ContextoBanco
from app.database.models import Medidas, Localizacao
from app.services.mqtt import setup_mqtt


mqttc = setup_mqtt()

@asynccontextmanager
async def lifespan(app: FastAPI):
    mqttc.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqttc.loop_start()
    yield
    mqttc.loop_stop()
    mqttc.disconnect()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/obter-ultimo")
def obter_ultima_atualizacao():
    with ContextoBanco() as db:
        medida = db.query(Medidas).order_by(Medidas.id.desc()).first()
        localizacao = db.query(Localizacao).where(medida.id_localizacao == Localizacao.id).first()
        
        dados = {
            "localizacao": {
                "lat": localizacao.latitude,
                "long": localizacao.longitude,
                "precisao": localizacao.precisao
            },
            "medidas": medida
        }
        if not medida:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado")
        
        return dados