import network
import time
from machine import Pin, ADC, I2C
import dht
import ujson
from umqtt.simple import MQTTClient
import bmp085

# Configurações MQTT
ID_MQTT = "esp32-iot-estacao-unip"
BROKER_MQTT = "broker.hivemq.com"
USUARIO = ""
SENHA = ""
MQTT_TOPIC = "projeto-unip/estacao-meteorologica/temperatura"

# Sensores
sensor_dht = dht.DHT22(Pin(15))

# ADC1 (GPIO 35) para o LDR
ldr = ADC(Pin(35))
ldr.atten(ADC.ATTN_11DB)

# MQ-135
mq135_analogico = ADC(Pin(34))
mq135_analogico.atten(ADC.ATTN_11DB)
mq135_digital = Pin(13, Pin.IN)

# Pinos I2C no ESP32 (SCL=22, SDA=21)
i2c = I2C(0, scl=Pin(21), sda=Pin(22), freq=100000)

try:
    bmp = bmp085.BMP085(i2c)
    print("BMP180/BMP085 inicializado com sucesso!")
except Exception as e:
    bmp = None
    print("Erro ao inicializar BMP180:", e)


def conectar_wifi():

    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    if not wifi.isconnected():
        print("Conectando ao WIFI........")
        wifi.connect("Wokwi-GUEST", "")  # Informe o SSID da REDE e senha...
        tentativas = 0
        while not wifi.isconnected() and tentativas < 20:
            print(".", end="")
            time.sleep(0.5)
            tentativas += 1
            
    if wifi.isconnected():
        print("\nWi-Fi conectado! IP:", wifi.ifconfig()[0])
        return True
    else:
        print("\nFalha ao conectar no Wi-Fi!")
        return False


def conectar_mqtt():
    try:
        c = MQTTClient(
            ID_MQTT,
            BROKER_MQTT,
            user=USUARIO,
            password=SENHA,
            keepalive=60
        )
        c.connect()
        print("MQTT conectado!")
        return c
    except Exception as erro:
        print("Falha na conexão MQTT:", erro)
        return None


conectar_wifi()
client = conectar_mqtt()

while True:
    print("\n--------------------------------------------------")
    print("INICIANDO LEITURA DOS SENSORES..................")
    
    
    erros = []

    try:
        sensor_dht.measure()
        temperatura_dht = sensor_dht.temperature()
        umidade = sensor_dht.humidity()
        print("DHT22 -> Temp:", temperatura_dht, "°C | Umidade:", umidade, "%")
    except Exception as erro:
        print("Erro no DHT22:", erro)
        erros.append("DHT22: " + str(erro))
        temperatura_dht = None
        umidade = None

    try:
        if bmp:
            temperatura_bmp = bmp.temperature
            pressao_bmp = bmp.pressure
            print("BMP180 -> Temp:", temperatura_bmp, "°C | Pressao:", pressao_bmp, "Pa")
        else:
            temperatura_bmp = None
            pressao_bmp = None
    except Exception as erro:
        print("Erro no BMP180:", erro)
        erros.append("BMP180: " + str(erro))
        temperatura_bmp = None
        pressao_bmp = None


    try:
        valor_ldr = ldr.read()
        print("LDR -> Luminosidade:", valor_ldr)
    except Exception as erro:
        print("Erro no LDR:", erro)
        erros.append("LDR: " + str(erro))
        valor_ldr = None


    try:
        valor_mq135 = mq135_analogico.read()
        estado_mq135 = mq135_digital.value()
        print("MQ-135 -> Analogico:", valor_mq135, "| Digital:", estado_mq135)
    except Exception as erro:
        print("Erro no MQ-135:", erro)
        erros.append("MQ-135: " + str(erro))
        valor_mq135 = None
        estado_mq135 = None


    if len(erros) > 0:
        print("\nAvisos/Erros capturados nas leituras:")
        for err in erros:
            print(" -", err)


    dados = {
        "temperatura": str(temperatura_dht),
        "umidade": str(umidade),
        "pressao": str(pressao_bmp),
        "temperatura_bmp": str(temperatura_bmp),
        "luminosidade": str(valor_ldr),
        "gas": str(valor_mq135),
        "gas_digital": str(estado_mq135)
    }

    mensagem = ujson.dumps(dados)
    print("\nJSON Gerado:\n", mensagem)

   
    if not network.WLAN(network.STA_IF).isconnected():
        conectar_wifi()

    if client is None:
        client = conectar_mqtt()
    else:
        try:
            client.publish(MQTT_TOPIC, mensagem)
            print("Dados enviados com sucesso via MQTT!")
            print(mensagem)
        except Exception as erro:
            print("Erro ao enviar MQTT:", erro)
            client = conectar_mqtt()

    time.sleep(5)