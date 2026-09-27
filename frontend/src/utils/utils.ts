export function formatarData(data: string): string {
    const [ano, mes, resto] = data.split("-");
    const [dia, hora] = resto.split(" ");

    return `${dia}/${mes}/${ano} ${hora}`;
}
