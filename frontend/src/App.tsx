
import './App.css';
import Card from './components/Card';
import GasCard from './components/GasCard';
import LuminosidadeCard from './components/LuminosidadeCard';
import PressaoCard from './components/PressaoCard';
import TemperaturaCard from './components/TemperaturaCard';
import UmidadeCard from './components/UmidadeCard';
import { useState } from 'react';
import { formatarData } from './utils/utils';
import GraficoChart from './components/GraficoChart';

interface Medidas {
    pressao: string;
    temperatura: string;
    umidade: string;
    temperatura_bmp: string;
    luminosidade: string;
    gas: string;
    gas_digital: string;
    data_cadastro: string;
}

export function App() {
    const [erro, setErro] = useState("");
    const [medida, setMedida] = useState<Medidas | null>(null);
    const [abaAtiva, setAbaAtiva] = useState<'medicoes' | 'graficos'>('medicoes');

    //Criar a requisição...
    // const obterMedidas = async () => {
    //     try {
    //         const request = await api.get("obter-ultimo");
    //         const response = request.data as Medidas;
    //
    //         setMedida(response);
    //     }
    //     catch (error: any) {
    //         console.error(error);
    //         setErro(error.response?.data);
    //     }
    // }

    // useEffect(() => {
    //     obterMedidas();
    // }, []);

    return (
        <main className="container py-2">
            <h1 className="text-center mb-3">
                Estação Meteorológica
            </h1>

            {medida && (
                <h3 className="text-center mb-3">
                    Última Atualização: {formatarData(medida.data_cadastro)}
                </h3>
            )}

            {erro && (
                <div className="alert alert-danger" role="alert">
                    {erro}
                </div>
            )}

            {/* Abas para dispositivos móveis */}
            <div className="nav nav-pills nav-fill mb-3 d-md-none">
                <button
                    type="button"
                    className={`nav-link ${abaAtiva === 'medicoes' ? 'active' : ''}`}
                    onClick={() => setAbaAtiva('medicoes')}
                >
                    <i className="fa fa-gauge-high me-2"></i>
                    Medições
                </button>

                <button
                    type="button"
                    className={`nav-link ${abaAtiva === 'graficos' ? 'active' : ''}`}
                    onClick={() => setAbaAtiva('graficos')}
                >
                    <i className="fa fa-chart-line me-2"></i>
                    Histórico
                </button>
            </div>

            {/* Primeira linha: Temperatura, Umidade e Gás */}
            <div className={`row g-2 mb-2 ${abaAtiva === 'medicoes' ? 'd-flex' : 'd-none'} d-md-flex`}>

                <div className="col-12 col-md-4">
                    <Card
                        titulo="Temperatura"
                        explicacao={
                            <>
                                <p>
                                    A temperatura ambiente é medida pelo sensor
                                    <strong> DHT22</strong> e apresentada em graus Celsius (°C).
                                </p>

                                <h6>Como funciona a medição?</h6>

                                <p>
                                    O DHT22 utiliza um sensor interno para medir a temperatura
                                    do ambiente e transmite os dados ao ESP32.
                                </p>

                                <h6>Sobre os valores</h6>

                                <ul>
                                    <li><strong>Baixa:</strong> temperatura abaixo da faixa de referência.</li>
                                    <li><strong>Agradável:</strong> temperatura dentro da faixa de referência.</li>
                                    <li><strong>Elevada:</strong> temperatura acima da faixa de referência.</li>
                                </ul>

                                <div className="alert alert-info mb-0">
                                    Os valores apresentados representam a temperatura detectada
                                    no local onde a estação está instalada.
                                </div>
                            </>
                        }
                    >
                        {/* <TemperaturaCard temperatura={medida ? Number(medida.temperatura) : 0} /> */}
                        <TemperaturaCard temperatura={0} />
                    </Card>
                </div>

                <div className="col-12 col-md-4">
                    <Card
                        titulo="Umidade"
                        explicacao={
                            <>
                                <p>
                                    A umidade relativa do ar é medida pelo sensor
                                    <strong> DHT22</strong> e apresentada em porcentagem (%).
                                </p>

                                <h6>O que é umidade relativa?</h6>

                                <p>
                                    Representa a quantidade de vapor de água presente no ar
                                    em relação à quantidade máxima que ele pode conter
                                    naquela temperatura.
                                </p>

                                <h6>Sobre os valores</h6>

                                <ul>
                                    <li><strong>Abaixo de 30%:</strong> umidade baixa.</li>
                                    <li><strong>De 30% a 60%:</strong> umidade adequada.</li>
                                    <li><strong>Acima de 60%:</strong> umidade elevada.</li>
                                </ul>

                                <div className="alert alert-info mb-0">
                                    As faixas são referências simplificadas para interpretação
                                    da umidade relativa do ar em ambientes internos.
                                </div>
                            </>
                        }
                    >
                        {/* <UmidadeCard umidade={medida ? Number(medida.umidade) : 0} /> */}
                        <UmidadeCard umidade={0} />
                    </Card>
                </div>

                <div className="col-12 col-md-4">
                    <Card
                        titulo="Gás - Qualidade do Ar"
                        explicacao={
                            <>
                                <p>
                                    O <strong>MQ-135</strong> é um sensor utilizado para detectar
                                    variações na presença de determinados gases no ambiente.
                                </p>

                                <h6>Como funciona a medição?</h6>

                                <p>
                                    O ESP32 recebe um sinal analógico do sensor e converte
                                    essa leitura em um valor digital (ADC), que varia de
                                    <strong> 0 a 4095</strong>.
                                </p>

                                <h6>Limitações do sensor</h6>

                                <ul>
                                    <li>Não fornece diretamente o Índice de Qualidade do Ar (AQI).</li>
                                    <li>Não identifica individualmente todos os gases.</li>
                                    <li>Sua resposta pode sofrer influência da temperatura e umidade.</li>
                                    <li>Necessita de calibração para uma interpretação mais precisa.</li>
                                </ul>

                                <div className="alert alert-warning mb-0">
                                    <strong>Atenção:</strong> a leitura é experimental e representa
                                    a resposta elétrica do sensor. Não deve ser utilizada para
                                    determinar se o ar é seguro ou prejudicial à saúde.
                                </div>
                            </>
                        }
                    >
                        {/* <GasCard adc={medida ? Number(medida.gas) : 0} /> */}
                        <GasCard adc={0} />
                    </Card>
                </div>
            </div>

            {/* Segunda linha: Luminosidade e Pressão */}
            <div className={`row g-2 mb-2 ${abaAtiva === 'medicoes' ? 'd-flex' : 'd-none'} d-md-flex`}>

                <div className="col-12 col-md-6">
                    <Card
                        titulo="Luminosidade"
                        explicacao={
                            <>
                                <p>
                                    A luminosidade é detectada por um <strong>LDR</strong>,
                                    componente cuja resistência elétrica varia conforme
                                    a quantidade de luz recebida.
                                </p>

                                <h6>Como funciona a medição?</h6>

                                <p>
                                    O ESP32 realiza a leitura analógica do circuito e converte
                                    o sinal em um valor digital (ADC), entre
                                    <strong> 0 e 4095</strong>.
                                </p>

                                <h6>Como interpretar os valores?</h6>

                                <ul>
                                    <li><strong>ADC baixo:</strong> maior luminosidade.</li>
                                    <li><strong>ADC intermediário:</strong> luminosidade moderada.</li>
                                    <li><strong>ADC alto:</strong> menor luminosidade.</li>
                                </ul>

                                <div className="alert alert-info mb-0">
                                    No circuito utilizado, a leitura ADC aumenta quando a
                                    luminosidade diminui. O valor apresentado não representa
                                    lux, pois não foi realizada uma conversão calibrada.
                                </div>
                            </>
                        }
                    >
                        {/* <LuminosidadeCard lux={medida ? Number(medida.luminosidade) : 0} /> */}
                        <LuminosidadeCard lux={0} />
                    </Card>
                </div>

                <div className="col-12 col-md-6">
                    <Card
                        titulo="Pressão"
                        explicacao={
                            <>
                                <p>
                                    A pressão atmosférica é medida pelo sensor
                                    <strong> BMP280</strong>, responsável por detectar
                                    a pressão exercida pelo ar no ambiente.
                                </p>

                                <h6>Como funciona a medição?</h6>

                                <p>
                                    O BMP280 utiliza um elemento sensor interno para medir
                                    a pressão atmosférica e transmite os dados ao ESP32
                                    por comunicação I2C.
                                </p>

                                <h6>Sobre os valores</h6>

                                <ul>
                                    <li><strong>Pressão baixa:</strong> valor inferior à faixa de referência.</li>
                                    <li><strong>Pressão normal:</strong> valor próximo à faixa de referência.</li>
                                    <li><strong>Pressão elevada:</strong> valor superior à faixa de referência.</li>
                                </ul>

                                <div className="alert alert-info mb-0">
                                    A altitude influencia diretamente a pressão atmosférica.
                                    Por isso, a pressão medida localmente deve ser interpretada
                                    considerando a altitude da estação.
                                </div>
                            </>
                        }
                    >
                        {/* <PressaoCard hpa={medida ? Number(medida.pressao) : 0} /> */}
                        <PressaoCard hpa={0} />
                    </Card>
                </div>
            </div>

            {/* Histórico */}
            <div className={`row ${abaAtiva === 'graficos' ? 'd-flex' : 'd-none'} d-md-flex`}>
                <div className="col-12">
                    <div className="card p-3 shadow-sm">
                        <h4 className="mb-3">
                            Histórico de Medições
                        </h4>

                        <GraficoChart />
                    </div>
                </div>
            </div>
        </main>
    );
}

export default App;
