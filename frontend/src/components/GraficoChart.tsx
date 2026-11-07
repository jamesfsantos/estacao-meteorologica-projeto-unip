
'use client';

import {
	LineChart,
	Line,
	XAxis,
	YAxis,
	Tooltip,
	CartesianGrid,
	ResponsiveContainer,
	Legend
} from 'recharts';

import api from '../api/api';
import { useEffect, useState, useCallback } from 'react';
import DatePicker from 'react-datepicker';

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

// Converte Date para YYYY-MM-DD
function formatarDataFiltro(data: Date): string {
	const ano = data.getFullYear();
	const mes = String(data.getMonth() + 1).padStart(2, '0');
	const dia = String(data.getDate()).padStart(2, '0');

	return `${ano}-${mes}-${dia}`;
}

export default function GraficoChart() {

	const [medidas, setMedidas] = useState<Medidas[]>([]);
	const [data, setData] = useState<Date>(new Date());

	const obterMedidas = useCallback(async (data: Date) => {
		const dataFiltro = formatarDataFiltro(data);

		try {
			const request = await api.get(
				`obter-ultimas-medidas?data_filtro=${dataFiltro}`
			);

			const response = request.data.medidas as Medidas[];

			setMedidas(response);

		} catch (error: any) {
			if (error.response?.status === 404) {
				setMedidas([]);
				return;
			}

			console.error('Erro ao buscar medidas:', error);
			setMedidas([]);
		}
	}, []);

	// Busca as medidas sempre que a data mudar
	useEffect(() => {
		obterMedidas(data);
	}, [data, obterMedidas]);

	return (
		<>
			<label>Selecione a Data:</label>
			<DatePicker
				selected={data}
				onChange={(date: Date | null) => {
					if (date) {
						setData(date);
					}
				}}
				dateFormat="dd/MM/yyyy"
				placeholderText="Selecione uma data"
				popperPlacement="bottom-start"
			/>

			<br />

			{medidas.length === 0 ? (
				<div>Não foi realizado nenhuma medição para a data selecionada.</div>
			) : (
				<div style={{ width: '100%', height: 350 }}>
					<ResponsiveContainer>
						<LineChart data={medidas}>
							<CartesianGrid strokeDasharray="3 3" />
							<XAxis dataKey="horario" />
							<YAxis />
							<Tooltip />
							<Legend />

							<Line
								type="monotone"
								dataKey="temperatura"
								name="Temperatura(C.)"
								stroke="#f05006"
								strokeWidth={2}
							/>

							<Line
								type="monotone"
								dataKey="umidade"
								name="Umidade(%)"
								stroke="#08bbf1"
								strokeWidth={2}
							/>

							<Line
								type="monotone"
								dataKey="gas"
								name="Gas - Qualidade do Ar(AQI)"
								stroke="#034d0f"
								strokeWidth={2}
							/>

							<Line
								type="monotone"
								dataKey="luminosidade"
								name="Luminosidade(lux)"
								stroke="#dbdf02"
								strokeWidth={2}
							/>

							<Line
								type="monotone"
								dataKey="pressao"
								name="Pressao(hPa)"
								stroke="#810707"
								strokeWidth={2}
							/>
						</LineChart>
					</ResponsiveContainer>
				</div>
			)}
		</>
	);
}
