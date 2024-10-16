# myapp/urls.py
from django.urls import path
from .views import DailyReportMorningList, show_daily_reports

urlpatterns = [
    path('api/reports/', DailyReportMorningList.as_view(), name='daily_report_morning_list'),
    path('show_daily_reports/', show_daily_reports, name='show_daily_reports'),
]
# 今変更kodama