from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DadosTemperatura(BaseModel):
    temperatura: str
    umidade: str
    pressao: str
    temperatura_bmp: str
    luminosidade: str
    gas: str
    gas_digital: str
    
    
mock_temperatura = {
    "temperatura_bmp": "2.9", 
    "gas_digital": "0", 
    "pressao": "83747", 
    "luminosidade": "1001", 
    "gas": "3628", 
    "temperatura": "54.3", 
    "umidade": "72.5"
}

#model_valiade --> Converte o json para a classe que chamo
dados = DadosTemperatura.model_validate(mock_temperatura)


@app.get("/")
def read_root():
    return {"dados": dados}






