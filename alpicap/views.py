from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from .forms import ContactForm
from django.contrib import messages 


from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import ConsultationRequestForm
from .models import ConsultationRequest
import logging









from .forms import AcceptanceFormForm
from .models import AcceptanceForm

















# Create your views here.

def homepage(request):
    srv = Service.objects.all()
    contact = ContactForm()
    if request.method == 'POST':
        contact = ContactForm(request.POST)
        if contact.is_valid():
            contact.save()
            messages.success(request,'Your message has been sent successfully, 🧑‍💻one of our representatives will get back to you shortly!!')
            return redirect('get_started')





    
    context = {
        'srv': srv,
        'contact': contact,

    }
 
    return render(request, 'index.html',context)




def get_started_view(request):
    """Render the get started page with the form"""
    form = ConsultationRequestForm()
    return render(request, 'get_started.html', {'form': form})

logger = logging.getLogger(__name__)

@require_http_methods(["POST"])
def submit_consultation_request(request):
    """Handle form submission via AJAX"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = ConsultationRequestForm(request.POST)
        
        if form.is_valid():
            consultation_request = form.save()
            
            # Send confirmation email to the client
            try:
                send_confirmation_email(consultation_request)
                
                # Send notification email to the admin
                send_admin_notification(consultation_request)
                
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you! We\'ll contact you within 24 hours to schedule your free consultation.'
                })
            except Exception as e:
                # Even if email fails, we still saved the request
                return JsonResponse({
                    'success': True,
                    'message': 'Your request has been submitted. We\'ll contact you soon!'
                })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors,
                'message': 'Please correct the errors below.'
            })
    else:
        # Handle regular form submission (non-AJAX)
        form = ConsultationRequestForm(request.POST)
        if form.is_valid():
            consultation_request = form.save()
            
            try:
                send_confirmation_email(consultation_request)
                send_admin_notification(consultation_request)
            except:
                pass  # Continue even if email fails
            
            messages.success(request, 'Thank you! We\'ll contact you within 24 hours to schedule your free consultation.')
            return redirect('get_started')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'get_started.html', {'form': form})


def send_confirmation_email(consultation_request):
    """Send confirmation email to the client"""
    subject = 'Consultation Request Received - Alpicap Investment Management'
    message = f"""
    Dear {consultation_request.full_name},

    Thank you for your interest in Alpicap Investment Management!

    We have received your consultation request with the following details:
    - Name: {consultation_request.full_name}
    - Email: {consultation_request.email}
    - Phone: {consultation_request.phone or 'Not provided'}
    - Investment Goal: {consultation_request.get_investment_goal_display()}

    One of our expert advisors will contact you within 24 hours to schedule your free consultation.

    Best regards,
    The Alpicap Team
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [consultation_request.email],
        fail_silently=False,
    )

def send_admin_notification(consultation_request):
    """Send notification email to admin"""
    subject = 'New Consultation Request - Alpicap'
    message = f"""
    New consultation request received:

    Name: {consultation_request.full_name}
    Email: {consultation_request.email}
    Phone: {consultation_request.phone or 'Not provided'}
    Investment Goal: {consultation_request.get_investment_goal_display()}
    Submitted: {consultation_request.created_at.strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],  # You'll need to set this in settings
        fail_silently=False,
    )












def acceptance_form_view(request):
    if request.method == 'POST':
        form = AcceptanceFormForm(request.POST)
        if form.is_valid():
            acceptance_form = form.save()
            messages.success(
                request, 
                f'Application submitted successfully! Your reference ID is: {acceptance_form.reference_id}'
            )
            return redirect('acceptance_form_success')
            

        else:
            # If it's an AJAX request, return errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
    else:
        form = AcceptanceFormForm()
    
    return render(request, 'acceptance_form.html', {'form': form})



def acceptance_form_success(request):

    return render(request, 'success.html')
 












