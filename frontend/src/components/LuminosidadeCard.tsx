import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSun } from '@fortawesome/free-solid-svg-icons';

interface Luminosidade {
    lux: number;
}

export default function LuminosidadeCard({ lux }: Luminosidade) {

    let status = "";
    let cor = "";

    if (lux < 1000) {
        status = "Muita luminosidade";
        cor = "text-warning";
    } else if (lux < 2500) {
        status = "Luminosidade moderada";
        cor = "text-success";
    } else {
        status = "Pouca luminosidade";
        cor = "text-info";
    }

    return (
        <div className="text-center py-2">
            <div className="mb-2 text-warning">
                <FontAwesomeIcon size="3x" icon={faSun} />
            </div>

            <div className="fs-2 fw-semibold">
                {lux}
                <span className="fs-5 ms-1">ADC</span>
            </div>

            <div className={`mt-2 fw-semibold ${cor}`}>
                {status}
            </div>
        </div>
    );
}