import { faSun } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"

interface Luminosidade {
    lux: number;
}

export default function LuminosidadeCard({lux}: Luminosidade) {
    

    return <>
        <div className="alert" role="alert">
            <div className="text-center"><FontAwesomeIcon size="6x" icon={faSun} /></div>
            <div className="text-center display-1">{lux}<span className="fs-3">lux</span></div>
        </div>
    </>
}