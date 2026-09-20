import './App.css';
import Card from './components/Card';
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
            <TemperaturaCard temperatura={11} />
          </Card>
          <Card
            titulo='Umidade'
          >
            <UmidadeCard umidade={10}/>
          </Card>
        </div>
      </div>
    </main>
  );
}

export default App;