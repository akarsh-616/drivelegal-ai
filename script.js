// Premium Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Navigation Highlight Logic
const navLinks = document.querySelectorAll('.nav-links a');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    });
});

// Interactive Cursor Logic (Crosshair on face)
const faceBox = document.querySelector('.face-hitbox');
faceBox.addEventListener('mouseenter', () => {
    document.body.style.cursor = 'crosshair';
});
faceBox.addEventListener('mouseleave', () => {
    document.body.style.cursor = 'default';
});