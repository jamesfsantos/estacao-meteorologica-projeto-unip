export function formatarData(data: string): string {
    if (!data) return "";

    // Troca o 'T' por espaço caso ele exista na string
    const dataFormatada = data.replace("T", " ");
    
    const [ano, mes, resto] = dataFormatada.split("-");
    const [dia, hora] = resto.split(" ");

    return `${dia}/${mes}/${ano} às ${hora}`;
}

export function formatarDataFiltro(data: Date): string {
    const ano = data.getFullYear();
    const mes = String(data.getMonth() + 1).padStart(2, '0');
    const dia = String(data.getDate()).padStart(2, '0');

    return `${ano}-${mes}-${dia}`;
}