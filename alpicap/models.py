from django.db import models
from django.utils import timezone

from django.core.validators import EmailValidator, RegexValidator
import uuid










# Create your models here.

class CompanyProfile(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='logo')
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    copyright = models.CharField(max_length=50)
    about_company = models.TextField()
    time = models.CharField( max_length=50)
    logo = models.ImageField( upload_to='logo',default='av.png')
        
    def __str__(self):
            return self.name
    class Meta:
        db_table = 'CompanyProfile'
        managed = True
        verbose_name = 'CompanyProfile'
        verbose_name_plural = 'CompanyProfile'

class Service(models.Model):
    title = models.CharField(max_length=50)
    context = models.TextField()
    img = models.CharField(max_length=50)

        
    def __str__(self):
            return self.title
    class Meta:
        db_table = 'Service'
        managed = True
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

class Contact(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=50)
    subject= models.CharField(max_length=50)
    message = models.TextField()
    sent = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'contact'
        managed = True
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact'




class ConsultationRequest(models.Model):
    INVESTMENT_GOALS = [
        ('retirement', 'Retirement Planning'),
        ('wealth-building', 'Wealth Building'),
        ('income', 'Generate Income'),
        ('education', 'Education Funding'),
        ('other', 'Other'),
    ]


    
    
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    investment_goal = models.CharField(max_length=20, choices=INVESTMENT_GOALS)
    created_at = models.DateTimeField(default=timezone.now)
    is_contacted = models.BooleanField(default=False)
   



    class Meta:
        db_table = 'Get Started Submission'
        managed = True
        ordering = ['-created_at']
        verbose_name = "Get Started Submission"
        verbose_name_plural = "Get Started Submissions"
    
    def __str__(self):
        return f"{self.full_name} - {self.email}"
    










class AcceptanceForm(models.Model):
    INVESTMENT_GOAL_CHOICES = [
        ('retirement', 'Retirement Planning'),
        ('wealth', 'Wealth Building'),
        ('income', 'Income Generation'),
        ('education', 'Education Funding'),
        ('other', 'Other'),
    ]
    
    RISK_TOLERANCE_CHOICES = [
        ('conservative', 'Conservative'),
        ('moderate', 'Moderate'),
        ('aggressive', 'Aggressive'),
    ]
    
    INVESTMENT_AMOUNT_CHOICES = [
        ('500-1500', '$500 - $1,500'),
        ('2500-5500', '$2,500 - $5,500'),
        ('6000-10000', '$6,000 - $10,000'),
        ('10000-40000', '$10,000 - $40,000'),
        ('50000-100000', '$50,000 - $100,000'),
        ('100000+', '$100,000+'),
    ]
    
    SERVICE_CHOICES = [
        ('portfolio-management', 'Portfolio Management'),
        ('wealth-planning', 'Wealth Planning'),
        ('tax-optimization', 'Tax Optimization'),
        ('estate-planning', 'Estate Planning'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True,
    validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Enter a valid phone number')]
    ) 
    
    # Investment Preferences
    investment_goal = models.CharField(max_length=20, choices=INVESTMENT_GOAL_CHOICES)
    risk_tolerance = models.CharField(max_length=20, choices=RISK_TOLERANCE_CHOICES)
    investment_amount = models.CharField(max_length=20, choices=INVESTMENT_AMOUNT_CHOICES)
    
    # Services (we'll handle multiple selections as a comma-separated string)
    services = models.TextField(blank=True, null=True, help_text="Comma-separated list of services")
    
    # Additional Information
    additional_info = models.TextField(blank=True, null=True)
    
    # System fields
    reference_id = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Acceptance Form"
        verbose_name_plural = "Acceptance Forms"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.reference_id}"
    
    def save(self, *args, **kwargs):
        if not self.reference_id:
            import random
            import string
            timestamp = str(int(timezone.now().timestamp()))[-8:]
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            self.reference_id = f"ALP-{timestamp}{random_part}"
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def services_list(self):
        if self.services:
            return [service.strip() for service in self.services.split(',')]
        return []






