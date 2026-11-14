import { useEffect } from "react";
import { MapContainer, Marker, Popup, TileLayer, Circle, useMap } from "react-leaflet";

// Coordenadas padrão de fallback (caso lat/long venham Zeradas)
const POSICAO_DEFAULT: [number, number] = [-23.55052, -46.633308];
const ZOOM_INICIAL = 15;

interface MapaEstacaoProps {
    lat?: number;
    long?: number;
    precisao?: number;
}

// Componente para ajustar o Leaflet ao redimensionar a tela
function AjustarTamanho() {
    const map = useMap();

    useEffect(() => {
        const container = map.getContainer();

        const observer = new ResizeObserver(() => map.invalidateSize());
        observer.observe(container);

        const timeout = setTimeout(() => map.invalidateSize(), 100);

        return () => {
            observer.disconnect();
            clearTimeout(timeout);
        };
    }, [map]);

    return null;
}

function RecentralizarMapa({ posicao }: { posicao: [number, number] }) {
    const map = useMap();

    useEffect(() => {
        if (posicao[0] !== 0 && posicao[1] !== 0) {
            map.flyTo(posicao, map.getZoom() || ZOOM_INICIAL);
        }
    }, [posicao, map]);

    return null;
}

function BotaoCentralizar({ posicao }: { posicao: [number, number] }) {
    const map = useMap();

    return (
        <button
            type="button"
            className="btn btn-light btn-sm shadow-sm botao-centralizar"
            title="Voltar para a estação"
            aria-label="Voltar para a estação"
            onClick={() => map.flyTo(posicao, ZOOM_INICIAL)}
        >
            <i className="fa fa-location-crosshairs" aria-hidden="true"></i>
        </button>
    );
}

export default function MapaEstacao({ lat, long, precisao }: MapaEstacaoProps) {
    // Valida se as coordenadas recebidas são válidas
    const temCoordenadasValidas = lat !== undefined && long !== undefined && (lat !== 0 || long !== 0);
    const posicao: [number, number] = temCoordenadasValidas ? [Number(lat), Number(long)] : POSICAO_DEFAULT;

    return (
        <div className="map-container">
            <MapContainer center={posicao} zoom={ZOOM_INICIAL} scrollWheelZoom={false} style={{ height: "100%", width: "100%" }}>
                <AjustarTamanho />
                <RecentralizarMapa posicao={posicao} />
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                
                {temCoordenadasValidas && (
                    <>
                        <Marker position={posicao}>
                            <Popup>
                                <strong>Estação Meteorológica</strong> <br />
                                Lat: {posicao[0]} <br />
                                Long: {posicao[1]} <br />
                                {precisao ? `Precisão: ±${precisao}m` : ''}
                            </Popup>
                        </Marker>

                        {/* Desenha o raio de precisão em metros ao redor do marcador */}
                        {precisao && precisao > 0 && (
                            <Circle
                                center={posicao}
                                radius={Number(precisao)}
                                pathOptions={{ color: '#0d6efd', fillColor: '#0d6efd', fillOpacity: 0.15 }}
                            />
                        )}
                    </>
                )}

                <BotaoCentralizar posicao={posicao} />
            </MapContainer>
        </div>
    );
}