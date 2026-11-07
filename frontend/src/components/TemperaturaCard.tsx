
import { faTemperature0 } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

interface Temperatura {
    temperatura: number;
}

export default function TemperaturaCard({ temperatura }: Temperatura) {

    let corTermometro = "";
    let status = "";

    if (temperatura < 18) {
        corTermometro = "text-primary";
        status = "Fria";
    } else if (temperatura <= 26) {
        corTermometro = "text-success";
        status = "Agradável";
    } else if (temperatura <= 32) {
        corTermometro = "text-warning";
        status = "Quente";
    }
    else {
        corTermometro = "text-danger";
        status = "Muito Quente";
    }





    return (
        <div className="text-center py-2">
            <FontAwesomeIcon
                className={`${corTermometro} mb-2`}
                size="3x"
                icon={faTemperature0}
            />

            <div className="fs-2 fw-semibold">
                {temperatura}
                <span className="fs-5 ms-1">°C</span>
            </div>

            <div className={`mt-2 fw-semibold ${corTermometro}`}>
                {status}
            </div>
        </div >
    );
}
