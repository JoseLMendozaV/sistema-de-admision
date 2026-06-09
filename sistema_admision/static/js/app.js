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