// Toggle checkbox functionality
function toggleCheckbox(item) {
    const checkbox = item.querySelector('input[type="checkbox"]');
    checkbox.checked = !checkbox.checked;
    item.classList.toggle('selected');
}

// Form validation
function validateForm() {
    const requiredFields = document.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        const errorElement = document.getElementById(field.id + 'Error');
        if (!field.value.trim()) {
            if (errorElement) {
                errorElement.style.display = 'block';
            }
            field.style.borderColor = '#ef4444';
            isValid = false;
        } else {
            if (errorElement) {
                errorElement.style.display = 'none';
            }
            field.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        }
    });

    // Email validation
    const email = document.getElementById('email');
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (email.value && !emailRegex.test(email.value)) {
        document.getElementById('emailError').textContent = 'Please enter a valid email address';
        document.getElementById('emailError').style.display = 'block';
        email.style.borderColor = '#ef4444';
        isValid = false;
    }

    return isValid;
}

// Form submission
document.getElementById('onboardingForm').addEventListener('submit', function(e) {
    if (!validateForm()) {
        e.preventDefault();
    } else {
        const submitBtn = document.getElementById('nextBtn');
        submitBtn.textContent = 'Processing...';
        submitBtn.disabled = true;
    }
});

// Real-time validation
document.querySelectorAll('input, select').forEach(input => {
    input.addEventListener('input', function() {
        const errorElement = document.getElementById(this.id + 'Error');
        if (this.value.trim()) {
            if (errorElement) {
                errorElement.style.display = 'none';
            }
            this.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        }
    });
});