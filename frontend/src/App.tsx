import './App.css';
import Card from './components/Card';
import GasCard from './components/GasCard';
import LuminosidadeCard from './components/LuminosidadeCard';
import PressaoCard from './components/PressaoCard';
import TemperaturaCard from './components/TemperaturaCard';
import UmidadeCard from './components/UmidadeCard';
import api from './api/api';
import { useEffect, useState } from 'react';
import { formatarData } from './utils/utils';

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
	const [medida, setMedida] = useState<Medidas | null>(null)

	//Criar a requisição...
	const obterMedidas = async () => {
		try {
			const request = await api.get("obter-ultimo");
			const response = request.data as Medidas;

			setMedida(response)
		}
		catch (error: any) {
			console.error(error);
			setErro(error.response?.data);
		}
	}


	useEffect(() => {
		obterMedidas()
	}, [])

	return (
		<main className="container border vh-100">
			<h1 className="text-center">Estação Meteorológica</h1><br/>
			{medida && (<h3 className='text-center'>Ultima Atualização: {formatarData(medida.data_cadastro)}</h3>)}
			{erro && (
				<div className="alert alert-danger" role="alert">
					{erro}
				</div>)
			}

			<div className=''>
				<div className='row border justify-content-between m-1'>
					<Card
						titulo='Temperatura'
					>
						<TemperaturaCard temperatura={medida ? Number(medida.temperatura) : 0} />
					</Card>
					<Card
						titulo='Umidade'
					>
						<UmidadeCard umidade={medida ? Number(medida.umidade) : 0} />
					</Card>
					<Card
						titulo="Gás - Qualidade do Ar"
					>
						<GasCard aqi={medida ? Number(medida.gas) : 0} />
					</Card>
				</div>
				<div className='row border justify-content-around m-1'>
					<Card titulo='Luminosidade'>
						<LuminosidadeCard lux={medida ? Number(medida.luminosidade) : 0} />
					</Card>
					<Card titulo='Pressão'>
						<PressaoCard hpa={medida ? Number(medida.pressao) : 0} />
					</Card>
				</div>
			</div>
		</main>
	);
}



export default App;