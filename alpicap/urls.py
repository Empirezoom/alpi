from django.urls import path
from . import views





urlpatterns = [
    path('',views.homepage,name='homepage'),

    path('get-started/', views.get_started_view, name='get_started'),
    path('submit-consultation/', views.submit_consultation_request, name='submit_consultation'),


    path('acceptance_form', views.acceptance_form_view, name='acceptance_form'),
    path('success/', views.acceptance_form_success, name='acceptance_form_success'),




]