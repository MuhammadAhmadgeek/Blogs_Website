/*!
 * Ahmad's Blog — Enhanced Animations & Interactions
 */

/* ─── Navbar scroll behaviour ──────────────────────────────── */
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    if (mainNav) {
        const headerHeight = mainNav.clientHeight;
        window.addEventListener('scroll', () => {
            const currentTop = document.body.getBoundingClientRect().top * -1;
            if (currentTop < scrollPos) {
                if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                    mainNav.classList.add('is-visible');
                } else {
                    mainNav.classList.remove('is-visible', 'is-fixed');
                }
            } else {
                mainNav.classList.remove('is-visible');
                if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                    mainNav.classList.add('is-fixed');
                }
            }
            scrollPos = currentTop;
        });
    }

    /* ─── Intersection Observer: fade-in-up ─────────────────── */
    const fadeTargets = document.querySelectorAll(
        '.post-preview-card, .comment-card, .about-card, .auth-card, ' +
        '.contact-card, .form-card, .my-post-card, .fade-in-up, ' +
        '.my-posts-header, .my-posts-empty'
    );
    const fadeObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, i) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                fadeObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    fadeTargets.forEach(el => fadeObserver.observe(el));

    /* ─── Masthead floating particles ────────────────────────── */
    const masthead = document.querySelector('header.masthead');
    if (masthead) {
        for (let i = 0; i < 12; i++) {
            const dot = document.createElement('span');
            dot.className = 'masthead-particle';
            dot.style.cssText = `
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                width: ${6 + Math.random() * 10}px;
                height: ${6 + Math.random() * 10}px;
                animation-delay: ${Math.random() * 4}s;
                animation-duration: ${4 + Math.random() * 4}s;
                opacity: ${0.15 + Math.random() * 0.25};
            `;
            masthead.appendChild(dot);
        }
    }

    /* ─── Tilt effect on post cards ─────────────────────────── */
    document.querySelectorAll('.post-preview-card, .my-post-card').forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const cx = rect.width / 2;
            const cy = rect.height / 2;
            const rotX = ((y - cy) / cy) * 3;
            const rotY = ((x - cx) / cx) * -3;
            card.style.transform = `perspective(800px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-4px)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });

    /* ─── Typing cursor on masthead h1 ──────────────────────── */
    const h1 = document.querySelector('header.masthead h1');
    if (h1 && h1.textContent.trim().length > 0) {
        h1.classList.add('typed-done');
    }

    /* ─── Ripple on buttons ──────────────────────────────────── */
    document.querySelectorAll('.btn-create-post, .btn-primary-custom, .btn-primary').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            ripple.className = 'btn-ripple';
            ripple.style.left = `${e.clientX - rect.left}px`;
            ripple.style.top = `${e.clientY - rect.top}px`;
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });

    /* ─── Counter animation on stats ────────────────────────── */
    document.querySelectorAll('[data-count]').forEach(el => {
        const target = parseInt(el.dataset.count);
        let count = 0;
        const step = Math.ceil(target / 40);
        const timer = setInterval(() => {
            count = Math.min(count + step, target);
            el.textContent = count;
            if (count >= target) clearInterval(timer);
        }, 30);
    });
});
