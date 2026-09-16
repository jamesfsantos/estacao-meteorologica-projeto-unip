interface Temperatura {
    temperatura: number
}
export default function TemperaturaCard({temperatura}: Temperatura){

    return <>
        <div>
            {temperatura}
        </div>
    </>
}