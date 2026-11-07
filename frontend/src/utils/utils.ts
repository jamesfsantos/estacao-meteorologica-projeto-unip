export function formatarData(data: string): string {
    const [ano, mes, resto] = data.split("-");
    const [dia, hora] = resto.split(" ");

    return `${dia}/${mes}/${ano} ${hora}`;
}

export function formatarDataFiltro(data: Date): string {
    const ano = data.getFullYear();
    const mes = String(data.getMonth() + 1).padStart(2, '0');
    const dia = String(data.getDate()).padStart(2, '0');

    return `${ano}-${mes}-${dia}`;
}