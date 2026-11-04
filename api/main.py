from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, datetime,timedelta
from typing import Optional
from app.core.config import ALLOWED_ORIGINS,MQTT_BROKER,MQTT_PORT
from app.database.connection import ContextoBanco
from app.database.models import Medidas, Localizacao
from app.services.mqtt import setup_mqtt
from sqlalchemy import func


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

@app.get("/obter-ultimas-medidas")
def obter_ultimas_medidas(
    data_filtro: Optional[date] = Query(default=None, description="Data no formato YYYY-MM-DD")
):
    with ContextoBanco() as db:
        data_alvo = data_filtro or date.today()
        
        inicio = datetime.combine(data_alvo, datetime.min.time())
        fim = inicio + timedelta(days=1)
        
        print(data_alvo)
        medidas_db = db.query(Medidas).filter(Medidas.data_cadastro >= inicio, Medidas.data_cadastro < fim).all()

        medidas = []
        
        horarios = set()

        for medida in medidas_db:
            horario = medida.data_cadastro.strftime("%H:%M")
            if(horario not in horarios):
                horarios.add(horario)
                medidas.append(medida)
                
            if(len(medidas) == 5):
                break
            
            
        if not medidas:
            raise HTTPException(status_code=404,detail=f"Não foi encontrada nenhuma medida no dia: {data_alvo}!!")
        
        localizacao = medidas[0].localizacao
        
        dados = {
            "localizacao":{
                "latitude": localizacao.latitude,
                "longitude": localizacao.longitude,
                "precisao": localizacao.precisao
            },
            "medidas": [{
                "id": m.id,
                "umidade": m.umidade,
                "temperatura_bmp": m.temperatura_bmp,
                "gas": m.gas,
                "horario": m.data_cadastro.strftime("%H:%M"),
                "pressao": m.pressao,
                "temperatura": m.temperatura,
                "luminosidade": m.luminosidade,
                "gas_digital": m.gas_digital,
                "id_localizacao": m.id_localizacao
            }
            for m in medidas
            ]
        }
        
        return dados

@app.get("/obter-ultimo")
def obter_ultima_atualizacao():
    with ContextoBanco() as db:
        medida = db.query(Medidas).order_by(
            Medidas.id.desc()
        ).first()

        if not medida:
            raise HTTPException(
                status_code=404,
                detail="Nenhum registro encontrado"
            )

        localizacao = medida.localizacao

        dados = {
            "localizacao": {
                "lat": localizacao.latitude,
                "long": localizacao.longitude,
                "precisao": localizacao.precisao 
            },
            "medidas": {
                "id": medida.id,
                "umidade": medida.umidade,
                "temperatura_bmp": medida.temperatura_bmp,
                "gas": medida.gas,
                "data_cadastro": medida.data_cadastro,
                "pressao": medida.pressao,
                "temperatura": medida.temperatura,
                "luminosidade": medida.luminosidade,
                "gas_digital": medida.gas_digital,
                "id_localizacao": medida.id_localizacao
            }
        }

        return dados
