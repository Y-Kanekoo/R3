# myapp/views.py

from django.shortcuts import render
from .models import DailyReportMorning

def show_daily_reports(request):
    # 例: reportsのデータを取得する処理
    reports =  DailyReportMorning.objects.all()  # reportsのリストを取得するロジックを追加
    return render(request, 'myapp/show_daily_reports.html', {'reports': reports})  # アプリ名を含めて指定
