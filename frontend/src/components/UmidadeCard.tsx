import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHandHoldingDroplet } from '@fortawesome/free-solid-svg-icons';

interface Umidade {
    umidade: number;
}
export default function UmidadeCard({umidade}: Umidade){

    return <>
        <div className="alert" role="alert">
            <div className="text-center"><FontAwesomeIcon size="6x" icon={faHandHoldingDroplet} /></div>
            <div className="text-center display-1">{umidade}%</div>
        </div>
    </>
}