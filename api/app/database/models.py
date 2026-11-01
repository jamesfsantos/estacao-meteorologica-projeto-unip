from sqlalchemy import Column, DateTime, Integer, Numeric, func, SmallInteger
from app.database.connection import Base

class Medidas(Base):
    __tablename__ = "medidas"

    id = Column(Integer, primary_key=True, index=True)
    temperatura = Column(Numeric(10,2), nullable=True)
    umidade = Column(Numeric(10,2), nullable=True)
    pressao = Column(Numeric(10,2), nullable=True)
    temperatura_bmp = Column(Numeric(10,2), nullable=True)
    luminosidade = Column(Integer, nullable=True)
    gas = Column(Integer, nullable=True)
    gas_digital = Column(SmallInteger, nullable=True)
    data_cadastro = Column(DateTime, nullable=True, server_default=func.now())
    id_localizacao = Column(Integer, nullable=True)
    
class Localizacao(Base):
    __tablename__ = "localizacao"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Numeric(10, 7), nullable=False)
    longitude = Column(Numeric(10, 7), nullable=False)
    precisao = Column(Numeric(10, 2), nullable=True)
    data_cadastro = Column(DateTime, server_default=func.now())
    