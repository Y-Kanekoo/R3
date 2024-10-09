from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.show_daily_reports, name='show_daily_reports'),
]