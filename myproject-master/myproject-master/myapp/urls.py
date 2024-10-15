# myapp/urls.py
from django.urls import path
from .views import DailyReportMorningList

urlpatterns = [
    path('api/reports/', DailyReportMorningList.as_view(),
         name='daily_report_morning_list'),
]
