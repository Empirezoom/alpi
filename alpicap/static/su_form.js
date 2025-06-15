// Add some interactive animation when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Animate the reference ID appearance
    setTimeout(() => {
        const referenceId = document.querySelector('.reference-id');
        referenceId.style.transform = 'scale(1.05)';
        setTimeout(() => {
            referenceId.style.transform = 'scale(1)';
        }, 200);
    }, 500);
});