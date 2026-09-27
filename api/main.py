from contextlib import asynccontextmanager
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer,DateTime, create_engine, func
from sqlalchemy.orm import Session, declarative_base, sessionmaker
import paho.mqtt.client as mqtt


# Configuração do Banco de Dados.
connection_string = "mysql+mysqlconnector://root:root@127.0.0.1:3306/estacao_meteorologica_db" # Depois verificar para ganhar em uma variavel de Ambiente .env
engine = create_engine(connection_string, connect_args={"init_command": "SET time_zone = 'America/Sao_Paulo'"})
ContextoBanco = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Criação da Tabela medidas
class Medidas(Base):
    __tablename__ = "medidas"
    id = Column(Integer, primary_key=True, index=True)
    temperatura = Column(String, nullable=True)
    umidade = Column(String, nullable=True)
    pressao = Column(String, nullable=True)
    temperatura_bmp = Column(String, nullable=True)
    luminosidade = Column(String, nullable=True)
    gas = Column(String, nullable=True)
    gas_digital = Column(String, nullable=True)
    data_cadastro = Column(DateTime, nullable=True, server_default=func.now()) #func é utilizado para chamar funções sql.

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
        
        with ContextoBanco() as db:
            medida = Medidas(
                temperatura = dados_estacao.temperatura,
                umidade = dados_estacao.umidade,
                pressao = dados_estacao.pressao,
                temperatura_bmp = dados_estacao.temperatura_bmp,
                luminosidade = dados_estacao.luminosidade,
                gas = dados_estacao.gas,
                gas_digital = dados_estacao.gas_digital,
                data_cadastro = func.now()
            ) # Sem a necessidade de chamar aqui, pois quando o objeto é montado, ele já atribui um valor a propriedade data_cadastro
            
            db.add(medida)
            db.commit()
            
            print("Salvo no Banco!")
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

#Liberar CORS...
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# def read_root():
#     return dados_estacao

@app.get("/obter-ultimo")
def obterUltimaAtualizacao():
    ## Obtendo ultimo registro
    with ContextoBanco() as db:
        medida = db.query(Medidas).order_by(Medidas.id.desc()).first()
        medida.data_cadastro = str(medida.data_cadastro)
    
    
    
    return medida