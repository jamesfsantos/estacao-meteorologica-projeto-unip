import { useState } from "react";

interface CardProps {
    titulo: string;
    children: React.ReactNode;
    explicacao?: React.ReactNode;
}

export default function Card({ titulo, children, explicacao }: CardProps) {

    const [mostrarModal, setMostrarModal] = useState(false);

    return (
        <>
            <div className="card h-100">
                <div className="card-header fs-5 py-2">
                    {titulo}
                </div>

                <div className="card-body p-2">
                    {children}
                </div>

                <div className="card-footer py-2 text-center">
                    <button
                        className="btn btn-link text-decoration-none p-0"
                        onClick={() => setMostrarModal(true)}
                    >
                        <i className="fa fa-info-circle me-1" aria-hidden="true"></i>
                        Informações
                    </button>
                </div>
            </div>

            {mostrarModal && (
                <>
                    <div className="modal-backdrop fade show"></div>

                    <div
                        className="modal fade show d-block"
                        tabIndex={-1}
                        role="dialog"
                        onClick={() => setMostrarModal(false)}
                    >
                        <div
                            className="modal-dialog modal-dialog-centered"
                            onClick={(e) => e.stopPropagation()}
                        >
                            <div className="modal-content">
                                <div className="modal-header">
                                    <h5 className="modal-title">{titulo}</h5>
                                    <button
                                        type="button"
                                        className="btn-close"
                                        aria-label="Fechar"
                                        onClick={() => setMostrarModal(false)}
                                    />
                                </div>

                                <div className="modal-body">
                                    {explicacao || "Informações sobre esta medição."}
                                </div>

                                <div className="modal-footer">
                                    <button
                                        type="button"
                                        className="btn btn-secondary"
                                        onClick={() => setMostrarModal(false)}
                                    >
                                        Fechar
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </>
            )}
        </>
    );
}