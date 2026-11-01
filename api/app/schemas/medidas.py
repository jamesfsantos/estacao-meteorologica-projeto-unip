from pydantic import BaseModel

class PayloadEsp32(BaseModel):
    temperatura: float = 0.0
    umidade: float = 0.0
    pressao: float = 0.0
    temperatura_bmp: float = 0.0
    luminosidade: int = 0
    gas: int = 0
    gas_digital: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    precisao: int = 0