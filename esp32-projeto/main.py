
import network
import time
import ujson
import urequests

from machine import Pin, ADC, I2C
from dht import DHT22
from umqtt.simple import MQTTClient
from bmp280 import BMP280


# ==================================================
# CONFIGURACOES
# ==================================================

ID_MQTT = "esp32-iot-estacao-unip"
BROKER_MQTT = "broker.hivemq.com"
USUARIO = ""
SENHA = ""

MQTT_TOPIC = "projeto-unip/estacao-meteorologica/temperatura"

WIFI_SSID = "Marcio_2.4G"
WIFI_SENHA = "@@58974314@@"


# ==================================================
# FUNCOES AUXILIARES
# ==================================================

def exibir_titulo(texto):
    print("\n" + "=" * 55)
    print("  " + texto)
    print("=" * 55)


# ==================================================
# INICIALIZACAO DOS SENSORES
# ==================================================

exibir_titulo("ESTACAO METEOROLOGICA ESP32")

print("[INFO] Inicializando sensores...")

# DHT22 - GPIO15
sensor_dht = DHT22(Pin(15))

# LDR - GPIO32
ldr_analogico = ADC(Pin(32))
ldr_analogico.atten(ADC.ATTN_11DB)

# MQ-135 - saida analogica AO GPIO34
mq135_analogico = ADC(Pin(34))
mq135_analogico.atten(ADC.ATTN_11DB)

# MQ-135 - saida digital DO GPIO13
mq135_digital = Pin(13, Pin.IN)

# BMP280 - SDA GPIO21 / SCL GPIO22
i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=100000
)

# Inicializacao do BMP280
try:

    print("[INFO] Procurando dispositivos I2C...")

    dispositivos = i2c.scan()

    print("[INFO] Dispositivos encontrados:", dispositivos)

    bmp = BMP280(i2c)

    print("[OK] BMP280 inicializado!")

except Exception as erro:

    bmp = None

    print("[ERRO] BMP280:", erro)


print("[OK] Sensores inicializados!")


# ==================================================
# CONEXAO WI-FI
# ==================================================

wifi = network.WLAN(network.STA_IF)


def conectar_wifi():

    exibir_titulo("CONEXAO WI-FI")

    try:

        if not wifi.active():

            print("[INFO] Ativando interface Wi-Fi...")

            wifi.active(True)
            time.sleep(2)

        if wifi.isconnected():

            print("[OK] Wi-Fi ja conectado!")
            print("[INFO] IP:", wifi.ifconfig()[0])

            return True

        print("[INFO] Rede:", WIFI_SSID)
        print("[INFO] Iniciando conexao...")

        try:

            wifi.disconnect()
            time.sleep(1)

        except:
            pass

        wifi.connect(WIFI_SSID, WIFI_SENHA)

        tentativas = 0

        while not wifi.isconnected() and tentativas < 20: 

            print(
                "[WI-FI] Tentativa:",
                tentativas + 1,
                "| Status:",
                wifi.status()
            )

            time.sleep(1)
            tentativas += 1

        if wifi.isconnected():

            configuracao = wifi.ifconfig()

            print("[OK] Wi-Fi conectado!")
            print("[INFO] IP:", configuracao[0])
            print("[INFO] Gateway:", configuracao[2])

            return True

        print("[ERRO] Falha na conexao Wi-Fi.")
        print("[INFO] Status final:", wifi.status())

        return False

    except Exception as erro:

        print("[ERRO] Conexao Wi-Fi:", erro)

        return False


# ==================================================
# CONEXAO MQTT
# ==================================================

def conectar_mqtt():

    exibir_titulo("CONEXAO MQTT")

    try:

        print("[INFO] Broker:", BROKER_MQTT)
        print("[INFO] Topico:", MQTT_TOPIC)
        print("[INFO] Conectando...")

        client = MQTTClient(
            ID_MQTT,
            BROKER_MQTT,
            user=USUARIO,
            password=SENHA,
            keepalive=60
        )

        client.connect()

        print("[OK] MQTT conectado com sucesso!")

        return client

    except Exception as erro:

        print("[ERRO] Falha na conexao MQTT:", erro)

        return None


# ==================================================
# GEOLOCALIZACAO WI-FI - BEACONDB
# ==================================================

def obter_coordenadas():

    exibir_titulo("GEOLOCALIZACAO WI-FI - BEACONDB")

    if not wifi.isconnected():

        print("[ERRO] Sem conexao Wi-Fi.")
        return None

    try:

        print("[1/4] Realizando scan das redes Wi-Fi...")

        redes = wifi.scan()

        print("[OK] Redes encontradas:", len(redes))

        # Ordena pelo RSSI: sinal mais forte primeiro
        redes = sorted(
            redes,
            key=lambda rede: rede[3],
            reverse=True
        )

        # Seleciona as quatro redes mais fortes
        redes = redes[:4]

        print("\n[2/4] Redes selecionadas:")

        lista_redes = []

        for indice, rede in enumerate(redes):

            ssid = rede[0].decode("utf-8", "ignore")
            bssid = ":".join("%02X" % b for b in rede[1])
            canal = rede[2]
            rssi = rede[3]

            lista_redes.append({
                "macAddress": bssid,
                "signalStrength": rssi,
                "channel": canal
            })

            print("---------------------------------------")
            print("Rede:", indice + 1)
            print("SSID:", ssid)
            print("BSSID:", bssid)
            print("Canal:", canal)
            print("Sinal:", rssi, "dBm")

        if len(lista_redes) == 0:

            print("[ERRO] Nenhuma rede encontrada.")

            return None

        # Montagem do payload
        body = {
            "considerIp": False,
            "wifiAccessPoints": lista_redes
        }

        print("\n[3/4] Enviando requisicao ao BeaconDB...")

        url = "https://api.beacondb.net/v1/geolocate"

        response = None

        try:

            response = urequests.post(
                url,
                data=ujson.dumps(body),
                headers={
                    "Content-Type": "application/json"
                }
            )

            status = response.status_code
            conteudo = response.text

            print("[INFO] HTTP Status:", status)

            if status == 200:

                resultado = ujson.loads(conteudo)

                localizacao = resultado.get("location")

                if not localizacao:

                    print("[ERRO] Resposta sem coordenadas.")
					
                    return None

                latitude = localizacao.get("lat")
                longitude = localizacao.get("lng")
                precisao = resultado.get("accuracy")

                print("\n[4/4] Localizacao obtida!")
                print("---------------------------------------")
                print("Latitude:", latitude)
                print("Longitude:", longitude)
                print("Precisao estimada:", precisao, "metros")
                print("---------------------------------------")

                return resultado

            else:

                print("[ERRO] BeaconDB não conseguiu estimar a localização.")
                print("[INFO] Resposta:", conteudo)

                return None

        finally:

            if response is not None:

                response.close()

    except Exception as erro:

        print("[ERRO] Falha na geolocalizacao:", erro)

        return None


# ==================================================
# INICIALIZACAO DAS CONEXOES
# ==================================================

if conectar_wifi():

    client = conectar_mqtt()

    # Geolocalizacao realizada uma vez na inicializacao
    localizacao = obter_coordenadas()

else:

    client = None
    localizacao = None


# ==================================================
# LOOP PRINCIPAL DA ESTACAO
# ==================================================

while True:

    exibir_titulo("NOVA LEITURA DA ESTACAO")

    erros = []

    temperatura_dht = None
    umidade = None

    temperatura_bmp = None
    pressao_bmp = None

    valor_ldr = None
    estado_ldr = None

    valor_mq135 = None
    estado_mq135 = None

    print("[INFO] Coletando dados dos sensores...\n")

    # ----------------------------------------------
    # DHT22
    # ----------------------------------------------

    try:

        sensor_dht.measure()

        temperatura_dht = sensor_dht.temperature()
        umidade = sensor_dht.humidity()

        print(
            "[DHT22] Temperatura:",
            temperatura_dht,
            "C | Umidade:",
            umidade,
            "%"
        )

    except Exception as erro:

        print("[ERRO] DHT22:", erro)

        erros.append("DHT22: " + str(erro))

    # ----------------------------------------------
    # BMP280
    # ----------------------------------------------

    try:

        if bmp:

            temperatura_bmp = bmp.temperature
            pressao_bmp = bmp.pressure / 1000

            print(
                "[BMP280] Temperatura:",
                temperatura_bmp,
                "C | Pressao:",
                pressao_bmp,
                "kPa"
            )

        else:

            print("[AVISO] BMP280 indisponivel.")

    except Exception as erro:

        print("[ERRO] BMP280:", erro)

        erros.append("BMP280: " + str(erro))

    # ----------------------------------------------
    # LDR
    # ----------------------------------------------

    try:

        valor_ldr = ldr_analogico.read()

        ldr_digital = Pin(32, Pin.IN)
        estado_ldr = ldr_digital.value()

        print(
            "[LDR] ADC:",
            valor_ldr,
            "| Digital:",
            estado_ldr
        )

        if estado_ldr == 1:

            print("[LDR] Luminosidade: Pouca luz")

        else:

            print("[LDR] Luminosidade: Muita luz")

    except Exception as erro:

        print("[ERRO] LDR:", erro)

        erros.append("LDR: " + str(erro))

    # ----------------------------------------------
    # MQ-135
    # ----------------------------------------------

    try:

        valor_mq135 = mq135_analogico.read()
        estado_mq135 = mq135_digital.value()

        print(
            "[MQ-135] Analógico:",
            valor_mq135,
            "| Digital:",
            estado_mq135
        )

    except Exception as erro:

        print("[ERRO] MQ-135:", erro)

        erros.append("MQ-135: " + str(erro))

    # ----------------------------------------------
    # ERROS DOS SENSORES
    # ----------------------------------------------

    if len(erros) > 0:

        print("\n[AVISOS] Problemas encontrados:")

        for erro in erros:

            print(" -", erro)

    # ----------------------------------------------
    # LOCALIZACAO
    # ----------------------------------------------

    latitude = None
    longitude = None
    precisao = None

    if localizacao:

        dados_localizacao = localizacao.get("location", {}) #Obtendo do Payload.

        latitude = dados_localizacao.get("lat")
        longitude = dados_localizacao.get("lng")
        precisao = localizacao.get("accuracy")

        print("\n[GEOLOCALIZACAO]")
        print("Latitude:", latitude)
        print("Longitude:", longitude)
        print("Precisao:", precisao, "metros")

    else:

        print("\n[AVISO] Localizacao indisponivel.")

    # ----------------------------------------------
    # MONTAGEM DO JSON
    # ----------------------------------------------

    dados = {

        "temperatura": temperatura_dht,
        "umidade": umidade,

        "pressao": pressao_bmp,
        "temperatura_bmp": temperatura_bmp,

        "luminosidade": valor_ldr,

        "gas": valor_mq135,
        "gas_digital": estado_mq135,

        "latitude": latitude,
        "longitude": longitude,
        "precisao": precisao
    }

    mensagem = ujson.dumps(dados)

    print("\n[INFO] JSON GERADO:")
    print(mensagem)

    # ----------------------------------------------
    # RECONEXAO WI-FI
    # ----------------------------------------------

    if not wifi.isconnected():

        print("\n[AVISO] Wi-Fi desconectado.")
        print("[INFO] Tentando reconectar...")

        client = None

        if conectar_wifi():

            print("[OK] Wi-Fi recuperado!")

            # Tenta obter a localizacao se ainda nao existir
            if localizacao is None:

                localizacao = obter_coordenadas()

    # ----------------------------------------------
    # RECONEXAO MQTT
    # ----------------------------------------------

    if wifi.isconnected() and client is None:

        print("\n[INFO] Tentando reconectar ao MQTT...")

        client = conectar_mqtt()

    # ----------------------------------------------
    # PUBLICACAO MQTT
    # ----------------------------------------------

    if wifi.isconnected() and client is not None:

        try:

            print("\n[MQTT] Publicando dados...")

            client.publish(
                MQTT_TOPIC,
                mensagem
            )

            print("[OK] Dados publicados com sucesso!")
            print("[MQTT] Topico:", MQTT_TOPIC)

        except Exception as erro:

            print("[ERRO] Falha ao publicar MQTT:", erro)

            try:

                client.disconnect()

            except:
                pass

            client = None

    else:

        print("\n[AVISO] Dados nao publicados. MQTT indisponivel.")

    print("\n[INFO] Proxima leitura em 5 segundos...")

    time.sleep(5)

