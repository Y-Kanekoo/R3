# myapp/views.py
from rest_framework import generics
from .models import Employee, Questionnaire, DailyReport, DailyReportAnswer
from .serializers import EmployeesSerializer,QuestionnairesSerializer,DailyReportsSerializer,DailyReportAnswersSerializer
from django.shortcuts import render
import requests

# class DailyReportMorningList(generics.ListAPIView):
#     queryset = DailyReportMorning.objects.all()
#     serializer_class = DailyReportMorningSerializer


# # APIからデータを取得し、テンプレートに表示するためのビュー
# def show_daily_reports(request):
#     # ローカルサーバー上のAPIエンドポイントからデータを取得
#     response = requests.get('http://127.0.0.1:8000/api/reports/')
#     data = response.json()  # APIから取得したデータをJSON形式で読み込む
#     return render(request, 'myapp/show_daily_reports.html', {'reports': data})


class EmployeesList(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeesSerializer

class QuestionnairesList(generics.ListAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnairesSerializer

class Daily_reportsList(generics.ListAPIView):
    queryset = DailyReport.objects.all()
    serializer_class = DailyReportsSerializer

class Daily_report_answersList(generics.ListAPIView):
    queryset = DailyReportAnswer.objects.all()
    serializer_class = DailyReportAnswersSerializer