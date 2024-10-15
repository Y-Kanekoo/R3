from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.show_daily_reports, name='show_daily_reports'),
    path('Daily_report_select/', views.Daily_report_select, name='Daily_report_select'),
]