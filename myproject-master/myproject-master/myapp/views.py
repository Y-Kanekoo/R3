# myapp/views.py
from rest_framework import generics
from .models import DailyReportMorning
from .serializers import DailyReportMorningSerializer
from django.shortcuts import render
import requests

class DailyReportMorningList(generics.ListAPIView):
    queryset = DailyReportMorning.objects.all()
    serializer_class = DailyReportMorningSerializer


# APIからデータを取得し、テンプレートに表示するためのビュー
def show_daily_reports(request):
    # ローカルサーバー上のAPIエンドポイントからデータを取得
    response = requests.get('http://127.0.0.1:8000/api/reports/')
    data = response.json()  # APIから取得したデータをJSON形式で読み込む
    return render(request, 'myapp/show_daily_reports.html', {'reports': data})