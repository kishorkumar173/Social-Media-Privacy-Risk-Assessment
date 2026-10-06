/**
 * Main Frontend Application Script
 * General UI initializations, active navigation handling, and global tooltips.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Highlight current active nav item
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('.nav-link');
    links.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            links.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        }
    });
});
