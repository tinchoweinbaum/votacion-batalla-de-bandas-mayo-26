async function actualizarUI() {
    try {
        const response = await fetch('/api/resultados');
        if (!response.ok) throw new Error("No se pudo obtener la API");
        const data = await response.json(); 

        for (const [id_batalla, bandas] of Object.entries(data)) {
            const total = bandas.reduce((sum, b) => sum + (b.votos || 0), 0);

            bandas.forEach(b => {
                const nombreBanda = String(b.banda).toLowerCase();
                const pct = total === 0 ? 0 : (b.votos / total) * 100;
                
                const barra = document.getElementById(`barra-${id_batalla}-${nombreBanda}`);
                const contador = document.getElementById(`count-${id_batalla}-${nombreBanda}`);

                if (barra) {
                    barra.style.height = pct + "%";
                }
                if (contador) {
                    contador.innerText = b.votos;
                }
            });
        }
    } catch (err) {
        console.error("Error en polling:", err);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    actualizarUI();
    setInterval(actualizarUI, 3000);
});