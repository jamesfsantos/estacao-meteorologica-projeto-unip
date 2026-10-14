interface CardProps {
    titulo: string;
    children: React.ReactNode
}

export default function Card({titulo, children}: CardProps){
    
    
    return <>
        <div className="card col m-1">
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