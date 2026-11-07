
import { faGaugeHigh } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

interface Pressao {
    hpa: number;
}

export default function PressaoCard({ hpa }: Pressao) {

    let cor = "";
    let status = "";

    if (hpa < 1000) {
        cor = "text-primary";
        status = "Pressão Baixa";
    } else if( hpa <= 1020) {
        cor = "text-success";
        status = "Pressão Normal";
    }
    else{
        cor = "text-warning";
        status = "Pressão Alta";
    }

    return (
        <div className="text-center py-2">
            <FontAwesomeIcon
                size="3x"
                icon={faGaugeHigh}
                className={cor}
            />

            <div className="fs-2 fw-semibold">
                {hpa}
                <span className="fs-5 ms-1">hPa</span>
            </div>

            <div className={`mt-2 fw-semibold ${cor}`}>
                {status}
            </div>
        </div>
    );
}
