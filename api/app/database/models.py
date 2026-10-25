from sqlalchemy import Column, DateTime, Integer, String, func
from database import Base

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
    data_cadastro = Column(DateTime, nullable=True, server_default=func.now())