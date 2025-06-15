// Form submission with loading state
document.getElementById('finalSubmissionForm').addEventListener('submit', function(e) {
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.textContent = 'Submitting...';
    submitBtn.disabled = true;
    
    // Add a small delay to show the loading state
    setTimeout(() => {
        // Form will be submitted after this delay
    }, 500);
});