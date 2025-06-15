let currentStep = 1;
const totalSteps = 3;
const formData = {};

// Update progress bar
function updateProgressBar() {
    const progress = (currentStep / totalSteps) * 100;
    document.getElementById('progressBar').style.width = progress + '%';
}

// Show specific step
function showStep(step) {
    document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
    document.getElementById(`step${step}`).classList.add('active');
    updateProgressBar();
}

// Validate current step
function validateStep(step) {
    const stepElement = document.getElementById(`step${step}`);
    const requiredFields = stepElement.querySelectorAll('[required]');
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
    if (step === 1) {
        const email = document.getElementById('email');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (email.value && !emailRegex.test(email.value)) {
            document.getElementById('emailError').textContent = 'Please enter a valid email address';
            document.getElementById('emailError').style.display = 'block';
            email.style.borderColor = '#ef4444';
            isValid = false;
        }
    }

    return isValid;
}

// Next step
function nextStep() {
    if (validateStep(currentStep)) {
        saveStepData(currentStep);
        currentStep++;
        if (currentStep === 3) {
            updateSummary();
        }
        showStep(currentStep);
    }
}

// Previous step
function prevStep() {
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
    }
}

// Save step data
function saveStepData(step) {
    const stepElement = document.getElementById(`step${step}`);
    const inputs = stepElement.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        if (input.type === 'checkbox') {
            if (!formData.services) formData.services = [];
            if (input.checked && !formData.services.includes(input.value)) {
                formData.services.push(input.value);
            }
        } else {
            formData[input.name] = input.value;
        }
    });
}

// Update summary
function updateSummary() {
    const summaryContent = document.getElementById('summaryContent');
    const services = formData.services ? formData.services.join(', ').replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) : 'None selected';
    
    summaryContent.innerHTML = `
        <h3>Application Summary</h3>
        <div class="summary-item">
            <span>Name:</span>
            <span>${formData.firstName} ${formData.lastName}</span>
        </div>
        <div class="summary-item">
            <span>Email:</span>
            <span>${formData.email}</span>
        </div>
        <div class="summary-item">
            <span>Phone:</span>
            <span>${formData.phone || 'Not provided'}</span>
        </div>
        <div class="summary-item">
            <span>Investment Goal:</span>
            <span>${formData.investmentGoal.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
        </div>
        <div class="summary-item">
            <span>Risk Tolerance:</span>
            <span>${formData.riskTolerance.charAt(0).toUpperCase() + formData.riskTolerance.slice(1)}</span>
        </div>
        <div class="summary-item">
            <span>Investment Amount:</span>
            <span>${formData.investmentAmount}</span>
        </div>
        <div class="summary-item">
            <span>Services:</span>
            <span>${services}</span>
        </div>
    `;
}

// Toggle checkbox
function toggleCheckbox(item) {
    const checkbox = item.querySelector('input[type="checkbox"]');
    checkbox.checked = !checkbox.checked;
    item.classList.toggle('selected');
}

// Generate reference ID
function generateReferenceId() {
    return 'ALP-' + Date.now().toString().slice(-8) + Math.random().toString(36).substr(2, 4).toUpperCase();
}

// Reset form
function resetForm() {
    currentStep = 1;
    document.getElementById('onboardingForm').reset();
    document.querySelectorAll('.checkbox-item').forEach(item => item.classList.remove('selected'));
    document.querySelectorAll('.error-message').forEach(error => error.style.display = 'none');
    showStep(1);
    // Clear form data
    Object.keys(formData).forEach(key => delete formData[key]);
}

// Form submission
// Keep most of your existing JavaScript, but modify the form submission:
document.getElementById('onboardingForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (validateStep(3)) {
        const submitBtn = document.getElementById('submitBtn');
        submitBtn.textContent = 'Submitting...';
        submitBtn.disabled = true;
        
        // Submit form via AJAX
        const formData = new FormData(this);
        
        fetch('{% url "acceptance_form" %}', {
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
                document.getElementById('referenceId').textContent = data.reference_id;
                document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
                document.getElementById('success').classList.add('active');
                document.getElementById('progressBar').style.width = '100%';
            } else {
                alert('Error submitting form. Please check your inputs.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        })
        .finally(() => {
            submitBtn.textContent = 'Submit Application';
            submitBtn.disabled = false;
        });
    }
});





// Initialize
updateProgressBar();

// Add input event listeners for real-time validation
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