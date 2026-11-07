import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHandHoldingDroplet } from '@fortawesome/free-solid-svg-icons';

interface Umidade {
    umidade: number;
}

export default function UmidadeCard({ umidade }: Umidade) {

    let status = "";
    let cor = "";

    if (umidade < 30) {
        status = "Umidade baixa";
        cor = "text-warning";
    } else if (umidade <= 60) {
        status = "Umidade adequada";
        cor = "text-success";
    } else {
        status = "Umidade elevada";
        cor = "text-danger";
    }

    return (
        <div className="text-center py-2">
            <div className="mb-2 text-info">
                <FontAwesomeIcon size="3x" icon={faHandHoldingDroplet} />
            </div>

            <div className="fs-2 fw-semibold">
                {umidade}
                <span className="fs-5 ms-1">%</span>
            </div>

            <div className={`mt-2 fw-semibold ${cor}`}>
                {status}
            </div>
        </div>
    );
}