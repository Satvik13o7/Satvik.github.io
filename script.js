// Simple blog functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Add active link highlighting
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.style.textDecoration = 'underline';
        }
    });

    // Add fade-in animation for post previews
    const posts = document.querySelectorAll('.post-preview');
    posts.forEach((post, index) => {
        post.style.opacity = '0';
        post.style.transform = 'translateY(20px)';
        setTimeout(() => {
            post.style.transition = 'opacity 0.5s, transform 0.5s';
            post.style.opacity = '1';
            post.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Add reading time estimate
    const postContent = document.querySelector('.post-content');
    if (postContent) {
        const text = postContent.textContent;
        const wordsPerMinute = 200;
        const words = text.trim().split(/\s+/).length;
        const readingTime = Math.ceil(words / wordsPerMinute);

        const metaDiv = postContent.querySelector('.post-meta');
        if (metaDiv) {
            const readingTimeSpan = document.createElement('span');
            readingTimeSpan.textContent = ` • ${readingTime} min read`;
            readingTimeSpan.style.marginLeft = '10px';
            metaDiv.appendChild(readingTimeSpan);
        }
    }

    console.log('Blog loaded successfully!');
});
