# Estação Meteorológica IoT com ESP32, MicroPython e MQTT

Sistema completo de monitoramento ambiental desenvolvido em **MicroPython** para **ESP32**. O dispositivo coleta métricas de múltiplos sensores (temperatura, umidade, pressão atmosférica, luminosidade e qualidade do ar) e transmite as leituras formatadas em **JSON** via protocolo **MQTT** para integração com dashboards e APIs backend.

## Hardware Utilizado e Pinagem

| Componente | Tipo / Protocolo | Pino no ESP32 | Descrição | 
| ----- | ----- | ----- | ----- | 
| **ESP32** | Microcontrolador | — | Placa principal com conectividade Wi-Fi | 
| **DHT22** | Digital (1-Wire) | GPIO 15 | Leitura de temperatura (°C) e umidade rel. (%) | 
| **LDR (Fotoresistor)** | Analógico (ADC1) | GPIO 35 | Leitura de intensidade de luminosidade (0–4095) | 
| **MQ-135** | Analógico + Digital | GPIO 34 (AOUT) / GPIO 13 (DOUT) | Monitoramento de qualidade do ar e presença de gases | 
| **BMP180 / BMP085** | I2C (`scl=22`, `sda=21`) | GPIO 22 (SCL) / GPIO 21 (SDA) | Leitura de pressão atmosférica (Pa) e temperatura (°C) | 

> **Atenção:** Os sensores analógicos (LDR e MQ-135) foram alocados nos pinos **ADC1** (GPIO 34 e 35). Evite usar pinos do ADC2 (como GPIO 4, 0, 2, 12, 14, etc.) em projetos com conectividade Wi-Fi ativada, pois o driver Wi-Fi bloqueia o uso do ADC2 no ESP32.

## Conceitos Importantes de Configuração

### Conversor Analógico-Digital (ADC)

O **ADC** converte o sinal elétrico contínuo (tensão) dos sensores em um número digital entre `0` e `4095` (resolução de 12 bits do ESP32).

* A função `atten(ADC.ATTN_11DB)` define a atenuação do pino para aceitar a faixa completa de **0 a 3.3V**. Sem isso, a escala de leitura fica limitada a 0 \~ 1.0V e satura rapidamente.

## Pré-requisitos e Bibliotecas

Para rodar este script no ESP32, certifique-se de carregar no firmware MicroPython os seguintes arquivos/módulos na memória interna do microcontrolador:

* **`umqtt.simple`**: Módulo cliente MQTT para MicroPython.

* **`bmp085.py`**: Driver para comunicação I2C com o sensor de pressão BMP180/BMP085.

## Como Executar

1. **Clone ou copie os arquivos** para o diretório do seu projeto no Thonny IDE ou ambiente de simulação (como Wokwi).

2. **Ajuste as credenciais Wi-Fi** no método `conectar_wifi()`:

   ```
   wifi.connect("NOME_DA_SUA_REDE", "SENHA_DA_REDE")
   
   ```

3. **Configure os parâmetros MQTT** se desejar usar um broker privado ou um tópico customizado:

   ```
   BROKER_MQTT = "broker.hivemq.com"
   MQTT_TOPIC = "projeto-unip/estacao-meteorologica/temperatura"
   
   ```

4. Faça o upload dos arquivos para o ESP32 e execute o arquivo `main.py`.

## Formato dos Dados Enviados (Payload JSON)

A cada iteração (padrão de 5 segundos), o firmware publica uma mensagem formatada em JSON no tópico configurado:

```
{
  "temperatura": "24.5",
  "umidade": "62.1",
  "pressao": "101325",
  "temperatura_bmp": "24.3",
  "luminosidade": "1850",
  "gas": "420",
  "gas_digital": "0"
}

```

## Arquitetura e Estrutura do Código

```
.
├── main.py                   # Script principal de leitura, reconexão e envio MQTT
├── bmp085.py                 # Driver I2C para a leitura do sensor BMP180
├── umqtt/
│   └── simple.py             # Módulo cliente MQTT
└── README.md                 # Documentação do projeto

```

### Principais Destaques do Código

1. **Isolamento de Exceções**: Cada sensor possui seu próprio bloco `try/except`, impedindo que uma falha em um sensor comprometa o funcionamento dos outros.

2. **Gerenciamento Limpo de Erros**: A lista `erros` é reinicializada a cada ciclo do loop `while True`. Isso impede o acúmulo de histórico de falhas antigas já resolvidas.

3. **Auto-Reconexão**: Verificação contínua de conexão com Wi-Fi e MQTT antes de realizar a publicação dos dados.