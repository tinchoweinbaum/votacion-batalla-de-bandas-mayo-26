window.onload = () => {
    const tarjetas = document.querySelectorAll('.card-resultado');
    tarjetas.forEach(tarjeta => {
        const columnas = tarjeta.querySelectorAll('.columna-banda');
        let total = 0;
        columnas.forEach(col => total += parseInt(col.getAttribute('data-votos')));
        columnas.forEach(col => {
            const v = parseInt(col.getAttribute('data-votos'));
            const barra = col.querySelector('.barra-progreso');
            const pct = total === 0 ? 0 : (v / total) * 100;
            setTimeout(() => { barra.style.height = pct + "%"; }, 100);
        });
    });
};