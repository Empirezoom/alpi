// Add some interactive effects
document.querySelectorAll('.step').forEach((step, index) => {
    step.style.animationDelay = `${index * 0.1}s`;
    step.classList.add('fade-in');
});



// Enhanced form submission with AJAX
document.getElementById('getStartedForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const button = this.querySelector('button[type="submit"]');
    const originalText = button.textContent;
    const formData = new FormData(this);
    
    button.textContent = 'Processing...';
    button.disabled = true;
    
    // Clear previous error messages
    document.querySelectorAll('.form-errors').forEach(el => el.remove());
    
    fetch('{% url "submit_consultation" %}', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            button.textContent = 'Consultation Scheduled!';
            button.style.background = '#10b981';
            
            setTimeout(() => {
                alert(data.message);
                button.textContent = originalText;
                button.disabled = false;
                button.style.background = '';
                this.reset();
            }, 2000);
        } else {
            // Display field errors
            for (const [field, errors] of Object.entries(data.errors)) {
                const fieldElement = document.getElementById(`id_${field}`);
                if (fieldElement) {
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'form-errors';
                    errors.forEach(error => {
                        const errorText = document.createElement('div');
                        errorText.textContent = error;
                        errorDiv.appendChild(errorText);
                    });
                    fieldElement.parentNode.appendChild(errorDiv);
                }
            }
            
            button.textContent = originalText;
            button.disabled = false;
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        button.textContent = originalText;
        button.disabled = false;
        alert('An error occurred. Please try again.');
    });
});

