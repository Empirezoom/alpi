from django.contrib import admin

from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import *




from .models import AcceptanceForm








# Register your models here.

class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','phone','address']
    prepopulated_fields = {'slug':('name',)}
    
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id','title','img','context']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name',  'email','phone','subject','message', 'sent']









@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 
        'email', 
        'phone_display',
        'investment_goal_display', 
        'created_at_display',
        'is_contacted',
        'days_since_submission'
    
    ]
    list_filter = [
        'investment_goal', 
        'is_contacted', 
        'created_at'
    ]
    search_fields = [
        'full_name', 
        'email', 
        'phone'
    ]
    readonly_fields = [
        'created_at',
        'days_since_submission'
    ]
    list_editable = ['is_contacted']
    ordering = ['-created_at']
    list_per_page = 25
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('full_name', 'email', 'phone'),
            'description': 'Basic contact details provided by the prospect'
        }),
        ('Investment Details', {
            'fields': ('investment_goal',),
            'description': 'Investment preferences and goals'
        }),
        ('Status & Tracking', {
            'fields': ('is_contacted', 'created_at', 'days_since_submission'),
            'description': 'Follow-up status and submission tracking'
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Optionally restrict deletion
        return request.user.is_superuser


    def phone_display(self, obj):
        """Display phone number or indicate if not provided"""
        return obj.phone if obj.phone else format_html('<em style="color: #666;">Not provided</em>')
    phone_display.short_description = 'Phone'
    
    def investment_goal_display(self, obj):
        """Display investment goal with nice formatting"""
        return obj.get_investment_goal_display()
    investment_goal_display.short_description = 'Investment Goal'
    
    def created_at_display(self, obj):
        """Display formatted creation date"""
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_display.short_description = 'Submitted'
    created_at_display.admin_order_field = 'created_at'
    
    def days_since_submission(self, obj):
        """Calculate and display days since submission"""
        days = (timezone.now() - obj.created_at).days
        if days == 0:
            return format_html('<span style="color: #28a745;">Today</span>')
        elif days == 1:
            return format_html('<span style="color: #ffc107;">1 day ago</span>')
        elif days <= 3:
            return format_html(f'<span style="color: #fd7e14;">{days} days ago</span>')
        else:
            return format_html(f'<span style="color: #dc3545;">{days} days ago</span>')
    days_since_submission.short_description = 'Age'
    
    def get_queryset(self, request):
        """Optimize database queries"""
        return super().get_queryset(request).select_related()
    
    def changelist_view(self, request, extra_context=None):
        """Add summary statistics to the admin list view"""
        extra_context = extra_context or {}
        
        # Calculate statistics
        total_submissions = ConsultationRequest.objects.count()
        contacted = ConsultationRequest.objects.filter(is_contacted=True).count()
        pending = total_submissions - contacted
        today_submissions = ConsultationRequest.objects.filter(
            created_at__date=timezone.now().date()
        ).count()
        
        extra_context['summary_stats'] = {
            'total': total_submissions,
            'contacted': contacted,
            'pending': pending,
            'today': today_submissions,
            'contact_rate': round((contacted / total_submissions * 100) if total_submissions > 0 else 0, 1)
        }
        
        return super().changelist_view(request, extra_context)
















@admin.register(AcceptanceForm)
class AcceptanceFormAdmin(admin.ModelAdmin):
    list_display = [
        'reference_id',
        'full_name',
        'email',
        'investment_goal',
        'risk_tolerance',
        'investment_amount',
        'created_at'
    ]
    
    list_filter = [
        'investment_goal',
        'risk_tolerance',
        'investment_amount',
        'created_at'
    ]
    
    search_fields = [
        'first_name',
        'last_name',
        'email',
        'reference_id'
    ]
    
    readonly_fields = [
        'reference_id',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = [
        ('Personal Information', {
            'fields': ['first_name', 'last_name', 'email', 'phone']
        }),
        ('Investment Preferences', {
            'fields': ['investment_goal', 'risk_tolerance', 'investment_amount', 'services']
        }),
        ('Additional Information', {
            'fields': ['additional_info']
        }),
        ('System Information', {
            'fields': ['reference_id', 'created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    date_hierarchy = 'created_at'
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'


















admin.site.register(CompanyProfile,CompanyProfileAdmin) 
admin.site.register(Service,ServiceAdmin) 
admin.site.register(Contact,ContactAdmin) 



admin.site.site_header = "Alpicap Investment Management Admin"
admin.site.site_title = "Alpicap Admin"
admin.site.index_title = "Investment Management Dashboard"