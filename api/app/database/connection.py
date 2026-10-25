from core.config import CONNECTION_STRING
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(
    CONNECTION_STRING,
    connect_args={"init_command": "SET time_zone = 'America/Sao_Paulo'"}
)

ContextoBanco = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()