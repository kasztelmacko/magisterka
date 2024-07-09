document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelectorAll('#item-types-container a').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
