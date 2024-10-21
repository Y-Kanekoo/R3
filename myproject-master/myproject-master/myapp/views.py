# myapp/views.py
from rest_framework import generics
from .models import Employee, Questionnaire, DailyReport, DailyReportAnswer, Threshold
from .serializers import EmployeesSerializer, QuestionnairesSerializer, DailyReportsSerializer, DailyReportAnswersSerializer, ThresholdsSerializer
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

# # APIからデータを取得し、テンプレートに表示するためのビュー


def show_employees(request):
    # ローカルサーバー上のAPIエンドポイントからデータを取得
    response = requests.get('http://127.0.0.1:8000/api/EmployeesList/')
    data = response.json()  # APIから取得したデータをJSON形式で読み込む
    return render(request, 'myapp/show_employees.html', {'employees': data})


class QuestionnairesList(generics.ListAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnairesSerializer


def show_questionnaires(request):
    response = requests.get('http://127.0.0.1:8000/api/QuestionnairesList/')
    data = response.json()  # APIから取得したデータをJSON形式で読み込む
    return render(request, 'myapp/show_questionnaires.html', {'questionnaires': data})


class Daily_report_answersList(generics.ListAPIView):
    queryset = DailyReportAnswer.objects.all()
    serializer_class = DailyReportAnswersSerializer


def show_report_answers(request):
    response = requests.get(
        'http://127.0.0.1:8000/api/Daily_report_answersList/')
    data = response.json()  # APIから取得したデータをJSON形式で読み込む
    return render(request, 'myapp/show_report_answers.html', {'answers': data})


class Daily_reportsList(generics.ListAPIView):
    queryset = DailyReport.objects.all()
    serializer_class = DailyReportsSerializer


def show_daily_reports(request):
    response = requests.get('http://127.0.0.1:8000/api/Daily_reportsList/')
    question_response = requests.get(
        'http://127.0.0.1:8000/api/QuestionnairesList/')
    data = response.json()  # APIから取得したデータをJSON形式で読み込む
    return render(request, 'myapp/show_daily_reports.html', {'reports': data})


class ThresholdsList(generics.ListAPIView):
    queryset = Threshold.objects.all()
    serializer_class = ThresholdsSerializer


def show_Thresholds(request):
    response = requests.get('http://127.0.0.1:8000/api/ThresholdsList/')
    data = response.json()  # APIから取得したデータをJSON形式で読み込む
    return render(request, 'myapp/show_thresholds.html', {'thresholds': data})
