from django.urls import path
from .views import DailyReportMorningList

urlpatterns = [
    path('reports/', views.show_daily_reports, name='show_daily_reports'),
    path('Daily_report_select/', views.Daily_report_select,
         name='Daily_report_select'),
    path('api/reports/', DailyReportMorningList.as_view(),
         name='daily_report_list'),  # APIエンドポイントを追加
]
