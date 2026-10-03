# estacao-meteorologica-projeto-unip

Nesse projeto estarão:
- API em Python(FAST Api)

A API contará com a biblioteca PAHO para "escutar" mensagens de um determinado canal.

- FRONTEND (React)

O Frontend será feito em React, seguindo com padronização de Componentes para melhor montagem do layout da Dashboard.


# Utilizar o Projeto na sua Máquina!

## API

### Tem que ter instalado

- UV: Para instalar.
    - WINDOWS ( powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" )  
    - LINUX/MAC ( curl -LsSf https://astral.sh/uv/install.sh | sh )
- Python
    
Com o projeto instalado na máquiona abra o projeto em /api
Abra um terminal e execute: uv sync


## Frontend

### Tem que ter instalado

- Node.JS

Entre em /frontend abra o terminal e execute: npm install


# Para rodar o Projeto

FRONTEND: npm run dev
API: uvicorn main:app --reload