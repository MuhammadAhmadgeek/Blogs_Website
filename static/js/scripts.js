/*!
 * Ahmad's Blog - Theme Scripts
 * Clean Blog v6.0.9 base + custom fixes
 */
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    if (!mainNav) return;
    const headerHeight = mainNav.clientHeight;

    window.addEventListener('scroll', function () {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if (currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                mainNav.classList.remove('is-visible', 'is-fixed'); // BUG FIX: was remove(['is-visible'])
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove('is-visible'); // BUG FIX: was remove(['is-visible'])
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });

    // Animate post cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.post-preview-card, .comment-card, .about-card, .auth-card, .contact-card, .form-card').forEach(el => {
        observer.observe(el);
    });
});
