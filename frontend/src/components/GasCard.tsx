import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faWind } from "@fortawesome/free-solid-svg-icons"

interface Gas {
    aqi: number;
}
export default function GasCard({aqi}: Gas){


    return <>
        <div className="alert" role="alert">
            <div className="text-center"><FontAwesomeIcon size="6x" icon={faWind} /></div>
            <div className="text-center display-1">{aqi}<span className="fs-3">AQI</span></div>
        </div>
    </>
}