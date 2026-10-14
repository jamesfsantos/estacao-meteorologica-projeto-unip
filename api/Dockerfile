FROM python:3.13-slim

WORKDIR /app

# Instala dependências do Python
RUN echo "Instalando dependências do Python......"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte da aplicação
COPY . .

RUN echo "Expondo porta 8080"
EXPOSE 5000

RUN echo "Rodando aplicação...."
# Executa o FastAPI com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]