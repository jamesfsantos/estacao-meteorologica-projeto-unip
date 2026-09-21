import './App.css';
import Card from './components/Card';
import GasCard from './components/GasCard';
import LuminosidadeCard from './components/LuminosidadeCard';
import PressaoCard from './components/PressaoCard';
import TemperaturaCard from './components/TemperaturaCard';
import UmidadeCard from './components/UmidadeCard';

export function App() {
  return (
    <main className="container border border-danger vh-100">
      <h1 className="text-center">Estação Meteorológica</h1>
      <div className=''>
        <div className='row border justify-content-between border-danger m-1'>
          <Card
            titulo='Temperatura'
          >
            <TemperaturaCard temperatura={30} />
          </Card>
          <Card
            titulo='Umidade'
          >
            <UmidadeCard umidade={10} />
          </Card>
          <Card
            titulo="Gás - Qualidade do Ar"
          >
            <GasCard aqi={10} />
          </Card>
        </div>
        <div className='row border justify-content-around border-danger m-1'>
          <Card titulo='Luminosidade'>
            <LuminosidadeCard lux={30}/>
          </Card>
          <Card titulo='Pressão'>
            <PressaoCard hpa={50}/>
          </Card>
        </div>
      </div>
    </main>
  );
}



export default App;