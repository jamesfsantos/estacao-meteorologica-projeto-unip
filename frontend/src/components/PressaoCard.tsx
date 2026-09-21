import { faClock } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

interface Pressao {
    hpa: number;
}
export default function PressaoCard({hpa}: Pressao){

    return <>
        <div className="alert" role="alert">
            <div className="text-center"><FontAwesomeIcon size="6x" icon={faClock} /></div>
            <div className="text-center display-1">{hpa}<span className="fs-3">hPa</span></div>
        </div>
    </>
}