'use client';

import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, Legend } from 'recharts';
import api from '../api/api';
import { useEffect, useState } from 'react';

interface Medidas {
	id: number;
	umidade: number;
	temperatura_bmp: number;
	gas: number;
	horario: string;
	pressao: number;
	temperatura: number;
	luminosidade: number;
	gas_digital: number;
	id_localizacao: number;
}



export default function GraficoChart() {

	const obterMedidas = async (data: string) => {
		const request = await api.get(`obter-ultimas-medidas?data_filtro=${data}`)
		console.log(request)
		const response = request.data.medidas as Medidas[]

		setMedidas(response)
	}


	useEffect(() => {
		obterMedidas(data)
	}, [])

	const [medidas, setMedidas] = useState<Medidas[]>([])
	const [data, setData] = useState(new Date().toISOString().split('T')[0])
	return (
		<>
			<div>Filtro: <input value={data} onChange={(e) => setData(e.target.value)} type='date' /> <button onClick={() => obterMedidas(data)}>Buscar</button></div>
			<br />
			{medidas.length == 0 ? <div>Nenhuma medida no dia</div> :
				<div style={{ width: '100', height: 350 }}>
					<ResponsiveContainer>
						<LineChart data={medidas}>
							<CartesianGrid strokeDasharray="3 3" />
							<XAxis dataKey="horario" />
							<YAxis />
							<Tooltip />
							<Legend />
							<Line type="monotone" dataKey="temperatura" name="Temperatura(C.)" stroke="#f05006" strokeWidth={2} />
							<Line type="monotone" dataKey="umidade" name="Umidade(%)" stroke="#08bbf1" strokeWidth={2} />
							<Line type="monotone" dataKey="gas" name="Gas-Qualidade de Ar(aqi)" stroke="#034d0f" strokeWidth={2} />
							<Line type="monotone" dataKey="luminosidade" name="Luminosidade(lux)" stroke="#dbdf02" strokeWidth={2} />
							<Line type="monotone" dataKey="pressao" name="Pressao(hPa)" stroke="#810707" strokeWidth={2} />
						</LineChart>
					</ResponsiveContainer>

				</div>

			}
		</>
	);
}
