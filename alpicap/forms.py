from django import forms 
from .models import Contact,ConsultationRequest
from django.core.exceptions import ValidationError



from .models import AcceptanceForm










class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact 
        fields = ['full_name', 'email', 'phone', 'subject','message',]




class ConsultationRequestForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = ['full_name', 'email', 'phone', 'investment_goal']
       
        labels = {
            'full_name': 'Full Name *',
            'email': 'Email Address *',
            'phone': 'Phone Number',
            'investment_goal': 'Investment Goal *',
        }


    
def clean_email(self):
    email = self.cleaned_data.get('email')
    if email:
        email = email.lower().strip()
    return email

def clean_full_name(self):
    name = self.cleaned_data.get('full_name')
    if name:
        name = name.strip().title()
    return name


def clean_phone(self):
    phone = self.cleaned_data.get('phone')
    if phone:
        # Remove any non-digit characters except + and -
        phone = ''.join(char for char in phone if char.isdigit() or char in ['+', '-', ' ', '(', ')'])
    return phone










class AcceptanceFormForm(forms.ModelForm):
    services = forms.MultipleChoiceField(
        choices=AcceptanceForm.SERVICE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Services of Interest"
    )
    
    class Meta:
        model = AcceptanceForm
        fields = [
            'first_name',
            'last_name', 
            'email',
            'phone',
            'investment_goal',
            'risk_tolerance',
            'investment_amount',
            'services',
            'additional_info'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g +15551234567'
            }),
            'investment_goal': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'risk_tolerance': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'investment_amount': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'additional_info': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us more about your investment goals or any questions you have...'
            })
        }
        
        labels = {
            'first_name': 'First Name *',
            'last_name': 'Last Name *',
            'email': 'Email Address *',
            'phone': 'Phone Number',
            'investment_goal': 'Primary Investment Goal *',
            'risk_tolerance': 'Risk Tolerance *',
            'investment_amount': 'Initial Investment Amount *',
            'additional_info': 'Additional Information'
        }
    
    def clean_services(self):
        services = self.cleaned_data.get('services')
        if services:
            return ','.join(services)
        return ''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add empty option to select fields
        self.fields['investment_goal'].empty_label = "Select your goal"
        self.fields['risk_tolerance'].empty_label = "Select risk level"
        self.fields['investment_amount'].empty_label = "Select amount"
        
        # If editing existing form, convert services string back to list
        if self.instance.pk and self.instance.services:
            self.initial['services'] = self.instance.services.split(',')











