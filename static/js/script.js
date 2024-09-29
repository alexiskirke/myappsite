document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Form submission
    const contactForm = document.getElementById('contact-form');
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(contactForm);
        const response = await fetch('/submit_contact', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        alert(result.message);
        contactForm.reset();
    });

    // Add a scroll reveal animation
    window.addEventListener('scroll', revealOnScroll);
});

function revealOnScroll() {
    const elements = document.querySelectorAll('.portfolio-item, #about, #contact');
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
        if (elementTop < windowHeight - 100) {
            element.classList.add('reveal');
        }
    });
}
