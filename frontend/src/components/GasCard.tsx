import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faWind } from "@fortawesome/free-solid-svg-icons";

interface Gas {
    adc: number;
}

export default function GasCard({ adc }: Gas) {

    let status = "";
    let cor = "";

    if (adc < 1000) {
        status = "Baixa concentração detectada";
        cor = "text-success";
    } else if (adc < 2500) {
        status = "Concentração moderada";
        cor = "text-warning";
    } else {
        status = "Alta resposta do sensor";
        cor = "text-danger";
    }

    return (
        <div className="text-center py-2">
            <FontAwesomeIcon
                size="3x"
                icon={faWind}
                className="text-success mb-2"
            />

            <div className="fs-2 fw-semibold">
                {adc}
                <span className="fs-5 ms-1">ADC</span>
            </div>

            <div className={`mt-2 fw-semibold ${cor}`}>
                {status}
            </div>
        </div>
    );
}