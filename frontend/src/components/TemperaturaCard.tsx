import { faTemperature0 } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { useState } from "react";

interface Temperatura {
    temperatura: number
}
export default function TemperaturaCard({temperatura}: Temperatura){

    //Icone mudará de cor a partir de uma certa temperatura
    
    let corTermometro = ""
    
    if(temperatura < 20){
        corTermometro = "text-primary"
    }else if(temperatura < 30){
        corTermometro = "text-warning"
    }else{
        corTermometro ="text-danger"
    }

    return <>
        <div className="alert" role="alert">
            <div className="text-center"><FontAwesomeIcon className={corTermometro}  size="6x" icon={faTemperature0} /></div>
            <div className="display-1 text-center">{temperatura}<span className='fs-1'>°C</span></div>
        </div>
    </>
}