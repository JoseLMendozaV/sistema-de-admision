document.addEventListener('DOMContentLoaded', function () {
    const progressBars = document.querySelectorAll('.progress-bar');

    progressBars.forEach(function (bar) {
        const width = bar.dataset.width || 0;
        bar.style.width = '0%';

        setTimeout(function () {
            bar.style.transition = 'width 700ms ease';
            bar.style.width = width + '%';
        }, 150);
    });

    const buscador = document.getElementById('buscadorAdmin');
    const cards = document.querySelectorAll('.estudiante-card');

    if (buscador) {
        buscador.addEventListener('input', function () {
            const texto = buscador.value.toLowerCase().trim();

            cards.forEach(function (card) {
                const contenido = card.dataset.search.toLowerCase();

                if (contenido.includes(texto)) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    }

    const botonesCopiar = document.querySelectorAll('.copiar-link');

    botonesCopiar.forEach(function (boton) {
        boton.addEventListener('click', async function () {
            const url = boton.dataset.url;

            try {
                await navigator.clipboard.writeText(url);
                const textoOriginal = boton.textContent;
                boton.textContent = 'Copiado';

                setTimeout(function () {
                    boton.textContent = textoOriginal;
                }, 1500);
            } catch (error) {
                alert('No se pudo copiar el enlace.');
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const formPerfil = document.querySelector('form[data-programas-url]');
    
    if (!formPerfil) {
        return;
    }

    const unidadSelect = document.getElementById('id_centro_regional');
    const programaSelect = document.getElementById('id_programa_postgrado');
    const programasUrl = formPerfil.dataset.programasUrl;

    if (!unidadSelect || !programaSelect || !programasUrl) {
        return;
    }

    unidadSelect.addEventListener('change', async function () {
        const unidadId = unidadSelect.value;

        programaSelect.innerHTML = '';
        programaSelect.disabled = true;

        const optionInicial = document.createElement('option');
        optionInicial.value = '';
        optionInicial.textContent = 'Cargando programas...';
        programaSelect.appendChild(optionInicial);

        if (!unidadId) {
            programaSelect.innerHTML = '';

            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'Seleccione primero la Facultad o Centro Regional';
            programaSelect.appendChild(option);

            return;
        }

        try {
            const response = await fetch(`${programasUrl}?unidad_id=${unidadId}`);
            const data = await response.json();

            programaSelect.innerHTML = '';

            const optionDefault = document.createElement('option');
            optionDefault.value = '';
            optionDefault.textContent = 'Seleccione un programa';
            programaSelect.appendChild(optionDefault);

            data.programas.forEach(function (programa) {
                const option = document.createElement('option');
                option.value = programa.id;
                option.textContent = programa.nombre;
                programaSelect.appendChild(option);
            });

            programaSelect.disabled = false;

        } catch (error) {
            programaSelect.innerHTML = '';

            const optionError = document.createElement('option');
            optionError.value = '';
            optionError.textContent = 'Error al cargar programas';
            programaSelect.appendChild(optionError);
        }
    });
});