from pydantic import BaseModel, ConfigDict

class DadosTemperatura(BaseModel):
    temperatura: str = "0.0"
    umidade: str = "0.0"
    pressao: str = "0"
    temperatura_bmp: str = "0.0"
    luminosidade: str = "0"
    gas: str = "0"
    gas_digital: str = "0"
