# myapp/views.py
from rest_framework import generics
from .models import Employee, Questionnaire, DailyReport, DailyReportAnswer, Threshold
from .serializers import EmployeesSerializer, QuestionnairesSerializer, DailyReportsSerializer, DailyReportAnswersSerializer, ThresholdsSerializer
from django.shortcuts import render
import requests



class EmployeesList(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeesSerializer

# # APIからデータを取得し、テンプレートに表示するためのビュー


def show_employees(request):
    # ローカルサーバー上のAPIエンドポイントからデータを取得
    response = requests.get('http://127.0.0.1:8000/api/EmployeesList/')
    employees = response.json()  # APIから取得したデータをJSON形式で読み込む
    return render(request, 'myapp/show_employees.html', {'employees': employees})


class QuestionnairesList(generics.ListAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnairesSerializer


def show_questionnaires(request):
    response = requests.get('http://127.0.0.1:8000/api/QuestionnairesList/')
    questionnaires = response.json()  # APIから取得したデータをJSON形式で読み込む
    return render(request, 'myapp/show_questionnaires.html', {'questionnaires': questionnaires})


class Daily_report_answersList(generics.ListAPIView):
    queryset = DailyReportAnswer.objects.all()
    serializer_class = DailyReportAnswersSerializer


def show_report_answers(request):
    response = requests.get('http://127.0.0.1:8000/api/Daily_report_answersList/')
    answers = response.json()  # APIから取得したデータをJSON形式で読み込む
    return render(request, 'myapp/show_report_answers.html', {'answers': answers})


class Daily_reportsList(generics.ListAPIView):
    queryset = DailyReport.objects.all()
    serializer_class = DailyReportsSerializer


def show_daily_reports(request):
    # レポートを取得
    reports = DailyReport.objects.select_related('employee').all()
    # 質問を取得
    questionnaires = Questionnaire.objects.all().order_by('id')  # 質問を順番に並べる
    # 回答を取得して質問の順にソート
    answers = DailyReportAnswer.objects.select_related('questionnaire').order_by('questionnaire__id')

    # レポートごとに回答を整理
    report_data = []
    for report in reports:
        report_answers = [
            {'question': answer.questionnaire.title, 'answer': answer.answer}
            for answer in answers if answer.daily_report_id == report.id
        ]
        report_data.append({
            'id': report.id,
            'employee': report.employee.name,
            'report_datetime': report.report_datetime,
            'report_type': report.report_type,
            'created_at': report.created_at,
            'updated_at': report.updated_at,
            'answers': report_answers  # リストとして回答を保持
        })

    # テンプレートに渡す
    return render(request, 'myapp/show_daily_reports.html', {
        'reports': report_data,
        'questionnaires': questionnaires,
    })






class ThresholdsList(generics.ListAPIView):
    queryset = Threshold.objects.all()
    serializer_class = ThresholdsSerializer


def show_Thresholds(request):
    response = requests.get('http://127.0.0.1:8000/api/ThresholdsList/')
    data = response.json()  # APIから取得したデータをJSON形式で読み込む
    return render(request, 'myapp/show_thresholds.html', {'thresholds': data})
