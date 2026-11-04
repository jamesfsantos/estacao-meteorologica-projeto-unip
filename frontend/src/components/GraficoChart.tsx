'use client';

import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, Legend } from 'recharts';

const dadosMeteorologicos = 
[
  {
    horario: '13:00',
    temperatura: 26,
    umidade: 60,
    gas:30,
    luminosidade:40,
    pressao:88,
  },
  {
    horario: '14:00',
    temperatura: 27,
    umidade: 70,
    gas:20,
    luminosidade:45,
    pressao:79,
  },
  {
    horario: '15:00',
    temperatura: 23,
    umidade: 50,
    gas:28,
    luminosidade:39,
    pressao:100,
  },
  {
    horario: '16:00',
    temperatura: 32,
    umidade: 43,
    gas:33,
    luminosidade:56,
    pressao:80,
  },
  {
    horario: '17:00',
    temperatura: 28,
    umidade: 66,
    gas:38,
    luminosidade:57,
    pressao:70,
  },
  {
    horario: '18:00',
    temperatura: 22,
    umidade: 59,
    gas:22,
    luminosidade:60,
    pressao:90,
  },
]

export default function GraficoChart(){
  return(
    <div style={{ width: '100', height: 350}}>
      <ResponsiveContainer>
        <LineChart data={dadosMeteorologicos}>
          <CartesianGrid strokeDasharray="3 3"/>
          <XAxis dataKey="horario"/>
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="temperatura" name="Temperatura(C.)" stroke="#f05006" strokeWidth={2} />
          <Line type="monotone" dataKey="umidade" name="Umidade(%)" stroke="#08bbf1" strokeWidth={2}/>
          <Line type="monotone" dataKey="gas" name="Gas-Qualidade de Ar(aqi)" stroke="#034d0f" strokeWidth={2}/>
          <Line type="monotone" dataKey="luminosidade" name="Luminosidade(lux)" stroke="#dbdf02" strokeWidth={2}/>
          <Line type="monotone" dataKey="pressao" name="Pressao(hPa)" stroke="#810707" strokeWidth={2}/>
        </LineChart>
      </ResponsiveContainer> 
    </div>
  );
}
