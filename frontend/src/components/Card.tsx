interface CardProps {
    titulo: string;
    children: React.ReactNode
}

export default function Card({titulo, children}: CardProps){


    return <>
        <div className="card col-3 m-3">
            <div className="card-header">{titulo}</div>
            <div className="card-body">
                {children}
            </div>
        </div>
    </>
}