import network
import time
import ujson

from machine import Pin, ADC, I2C
from dht import DHT22
from umqtt.simple import MQTTClient
from bmp280 import BMP280


# ==========================================
# CONFIGURAÇÕES MQTT
# ==========================================

ID_MQTT = "esp32-iot-estacao-unip"
BROKER_MQTT = "broker.hivemq.com"
USUARIO = ""
SENHA = ""
MQTT_TOPIC = "projeto-unip/estacao-meteorologica/temperatura"


WIFI_SSID = "WIFI_SSID"
WIFI_SENHA = "WIFI_SENHA"


# DHT22 - GPIO15
sensor_dht = DHT22(Pin(15))


# LDR - saída DO no GPIO32
ldr_analogico = ADC(Pin(32))
ldr_analogico.atten(ADC.ATTN_11DB)


# MQ-135 - saída analógica AO no GPIO34
mq135_analogico = ADC(Pin(34))
mq135_analogico.atten(ADC.ATTN_11DB)

# MQ-135 - saída digital DO no GPIO13
mq135_digital = Pin(13, Pin.IN)


# BMP280 - SDA GPIO21 / SCL GPIO22
i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=100000
)


# Inicialização do BMP280
try:
    print("Dispositivos I2C encontrados:", i2c.scan())

    bmp = BMP280(i2c)

    print("BMP280 inicializado com sucesso!")

except Exception as erro:
    bmp = None
    print("Erro ao inicializar BMP280:", erro)


wifi = network.WLAN(network.STA_IF)

def conectar_wifi():

    try:

        # Ativa a interface caso ainda esteja desativada
        if not wifi.active():
            wifi.active(True)
            time.sleep(2)

        if wifi.isconnected():
            print("Wi-Fi conectado! IP:", wifi.ifconfig()[0])
            return True

        print("Conectando à rede:", WIFI_SSID)

        # Evita chamar connect novamente se já houver uma tentativa em andamento
        try:
            wifi.disconnect()
            time.sleep(1)
        except:
            pass

        wifi.connect(WIFI_SSID, WIFI_SENHA)

        tentativas = 0

        while not wifi.isconnected() and tentativas < 20:

            print(
                "Tentativa:",
                tentativas + 1,
                "| Status:",
                wifi.status()
            )

            time.sleep(1)
            tentativas += 1

        if wifi.isconnected():

            print("Wi-Fi conectado! IP:", wifi.ifconfig()[0])
            return True

        print("Falha ao conectar. Status final:", wifi.status())
        return False

    except Exception as erro:

        print("Erro durante conexão Wi-Fi:", erro)
        return False



def conectar_mqtt():

    try:

        client = MQTTClient(
            ID_MQTT,
            BROKER_MQTT,
            user=USUARIO,
            password=SENHA,
            keepalive=60
        )

        client.connect()

        print("MQTT conectado!")

        return client

    except Exception as erro:

        print("Falha na conexão MQTT:", erro)
        return None



if conectar_wifi():
    client = conectar_mqtt()
else:
    client = None


while True:

    print("\n--------------------------------------------------")
    print("INICIANDO LEITURA DOS SENSORES..................")

    erros = []

    temperatura_dht = None
    umidade = None

    temperatura_bmp = None
    pressao_bmp = None

    valor_ldr = None
    estado_ldr = None

    valor_mq135 = None
    estado_mq135 = None


    try:

        sensor_dht.measure()

        temperatura_dht = sensor_dht.temperature()
        umidade = sensor_dht.humidity()

        print(
            "DHT22 -> Temp:",
            temperatura_dht,
            "°C | Umidade:",
            umidade,
            "%"
        )

    except Exception as erro:

        print("Erro no DHT22:", erro)

        erros.append("DHT22: " + str(erro))

        temperatura_dht = None
        umidade = None


    try:

        if bmp:

            temperatura_bmp = bmp.temperature
            pressao_bmp = bmp.pressure / 1000

            print(
                "BMP280 -> Temp:",
                temperatura_bmp,
                "°C | Pressão:",
                pressao_bmp,
                "kPa"
            )

        else:

            temperatura_bmp = None
            pressao_bmp = None

    except Exception as erro:

        print("Erro no BMP280:", erro)

        erros.append("BMP280: " + str(erro))

        temperatura_bmp = None
        pressao_bmp = None



    try:


        valor_ldr = ldr_analogico.read()

        ldr_digital = Pin(32, Pin.IN)
        estado_ldr = ldr_digital.value()

        print(
            "LDR -> ADC:",
            valor_ldr,
            "| DO:",
            estado_ldr
        )

        if estado_ldr == 1:
            print("Luminosidade: Pouca luz")
        else:
            print("Luminosidade: Muita luz")

    except Exception as erro:

        print("Erro no LDR:", erro)

        erros.append("LDR: " + str(erro))

        valor_ldr = None
        estado_ldr = None



    try:

        valor_mq135 = mq135_analogico.read()
        estado_mq135 = mq135_digital.value()

        print(
            "MQ-135 -> Analógico:",
            valor_mq135,
            "| Digital:",
            estado_mq135
        )

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

    if not wifi.isconnected():

        print("Wi-Fi desconectado. Tentando reconectar...")

        client = None

        if conectar_wifi():
            print("Wi-Fi recuperado!")
            
            
    if wifi.isconnected() and client is None:

        print("Tentando conectar ao MQTT...")

        client = conectar_mqtt()


    if wifi.isconnected() and client is not None:

        try:

            client.publish(MQTT_TOPIC, mensagem)

            print("Dados enviados com sucesso via MQTT!")
            print(mensagem)

        except Exception as erro:

            print("Erro ao enviar MQTT:", erro)

            try:
                client.disconnect()
            except:
                pass

            client = None


    time.sleep(5)
