import { useState } from "react";

interface CardProps {
    titulo: string;
    children: React.ReactNode
}

export default function Card({titulo, children}: CardProps){
    const [contador, setContador] = useState(0);

    
    return <>
        <div className="card col-3 m-3">
            <div className="card-header fs-5">{titulo}</div>
            <div className="card-body">
                {children}
                
            </div>
            <div className="card-footer">
                Rodapé
            </div>
        </div>
    </>
}