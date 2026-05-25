window.onload = () => {
    
    // Función de respaldo para UUID si el navegador bloquea crypto (ej. falta HTTPS)
    const generarUUID = () => {
        try {
            return crypto.randomUUID();
        } catch (e) {
            return 'voto-' + Math.random().toString(36).substr(2, 9) + Date.now().toString(36);
        }
    };

    // Función de alerta
    const mostrarAlerta = (mensaje) => {
        const cartelAlerta = document.getElementById("cartel-alerta");
        if (cartelAlerta) {
            cartelAlerta.textContent = mensaje;
            cartelAlerta.style.backgroundColor = "#fd521a";
            cartelAlerta.classList.add("mostrar");
            setTimeout(() => cartelAlerta.classList.remove("mostrar"), 3000);
        } else {
            alert(mensaje);
        }
    };

    // Lógica para marcar visualmente la opción seleccionada
    document.querySelectorAll('.opcion').forEach(opcion => {
        opcion.addEventListener('click', function() {
            const form = this.closest('form');
            form.querySelectorAll('.opcion').forEach(opt => opt.classList.remove('seleccionada'));
            this.classList.add('seleccionada');
        });
    });

    // Evento de clic para los botones de votar
    document.querySelectorAll('.btn-votar').forEach(boton => {
        boton.onclick = async (e) => {
            e.preventDefault();
            
            const form = boton.closest('form');
            const radio = form.querySelector('input[type="radio"]:checked');
            
            if (!radio) {
                mostrarAlerta("Elegí una banda primero");
                return;
            }

            // Gestión del ID de dispositivo con respaldo en memoria
            let id = localStorage.getItem('id_dispositivo');
            if (!id) {
                id = generarUUID();
                try { localStorage.setItem('id_dispositivo', id); } catch(e) {}
            }

            boton.textContent = "Procesando...";
            boton.disabled = true;

            const formData = new FormData();
            formData.append('id_banda', radio.value);
            formData.append('id_dispositivo', id);

            try {
                const response = await fetch('/votar', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok && data.status === "success") {
                    boton.textContent = "Voto emitido";
                    boton.classList.add('exito');
                    form.querySelectorAll('input').forEach(i => i.disabled = true);
                } else if (response.status === 403) {
                    boton.textContent = "Ya votaste";
                    boton.classList.add('bloqueado');
                    form.querySelectorAll('input').forEach(i => i.disabled = true);
                } else {
                    boton.textContent = "Votar";
                    boton.disabled = false;
                }
            } catch (err) {
                console.error("Error:", err);
                boton.textContent = "Votar";
                boton.disabled = false;
            }
        };
    });
};