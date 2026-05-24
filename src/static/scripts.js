document.addEventListener("DOMContentLoaded", () => {
    
    // Al seleccionar una opción, marcamos visualmente el contenedor
    document.querySelectorAll('.opcion').forEach(opcion => {
        const radio = opcion.querySelector('input[type="radio"]');
        radio.addEventListener('change', () => {
            const form = opcion.closest('form');
            form.querySelectorAll('.opcion').forEach(opt => opt.classList.remove('seleccionada'));
            opcion.classList.add('seleccionada');
        });
    });

    const cartelAlerta = document.getElementById("cartel-alerta");

    const mostrarAlerta = (mensaje, esExito = false) => {
        cartelAlerta.textContent = mensaje;
        cartelAlerta.style.backgroundColor = esExito ? "#28a745" : "#fd521a";
        cartelAlerta.classList.add("mostrar");
        setTimeout(() => cartelAlerta.classList.remove("mostrar"), 3000);
    };

    // Manejo de envío de formularios
    document.querySelectorAll('.formulario-voto').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const idBanda = formData.get('id_banda');
            const boton = form.querySelector('.btn-votar');
            
            if (!idBanda) {
                mostrarAlerta("Elegí una banda antes de votar, nabo");
                return;
            }
            
            boton.textContent = "Procesando...";
            boton.disabled = true;
            
            try {
                const response = await fetch('/votar', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    boton.textContent = "Voto emitido";
                    boton.classList.add('exito');
                    form.querySelectorAll('input').forEach(i => i.disabled = true);
                    mostrarAlerta("¡Voto registrado!", true);
                } else {
                    mostrarAlerta(data.message);
                    boton.textContent = "Votar en esta batalla";
                    boton.disabled = false;
                }
            } catch (err) {
                mostrarAlerta("Error de conexión");
                boton.textContent = "Votar en esta batalla";
                boton.disabled = false;
            }
        });
    });
});