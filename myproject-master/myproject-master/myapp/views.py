# myapp/views.py
from rest_framework import generics
from .models import Employee, Questionnaire, DailyReport, DailyReportAnswer, Threshold, Notification, send_notification
from .serializers import EmployeesSerializer, QuestionnairesSerializer, DailyReportsSerializer, DailyReportAnswersSerializer, ThresholdsSerializer, NotificationSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .forms import ThresholdForm
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from .forms import LoginForm


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
    response = requests.get(
        'http://127.0.0.1:8000/api/Daily_report_answersList/')
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
    answers = DailyReportAnswer.objects.select_related(
        'questionnaire').order_by('questionnaire__id')

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


def show_thresholds(request):
    thresholds = Threshold.objects.select_related(
        'employee', 'questionnaire').all()
    return render(request, 'myapp/show_thresholds.html', {'thresholds': thresholds})


def threshold_setting_view(request):
    if not request.user.employee.employee_type == 'admin':
        # 管理者でない場合、アクセス禁止
        return HttpResponseForbidden("あなたには、権限がありません。")
    if request.method == 'POST':
        form = ThresholdForm(request.POST)
        if form.is_valid():
            form.save()  # データを保存
            return redirect('threshold_list')  # 保存後、リスト画面にリダイレクト
    else:
        form = ThresholdForm()

    # テンプレートのパスを明示
    return render(request, 'myapp/threshold_setting.html', {'form': form})


def save_daily_report_answer_view(request):
    if request.method == 'POST':
        employee = Employee.objects.get(user=request.user)  # ログインユーザー（従業員）
        questionnaire_id = request.POST.get('questionnaire_id')
        answer_value = request.POST.get('answer_value')

        if not answer_value:
            # バリデーションチェック
            return render(request, 'error.html', {'message': 'Answer value is required'})

        answer_value = float(answer_value)

        # アンケート回答を保存
        report_answer = DailyReportAnswer.objects.create(
            daily_report_id=request.POST.get('daily_report_id'),
            questionnaire_id=questionnaire_id,
            answer=answer_value
        )

        # しきい値チェック
        try:
            threshold = Threshold.objects.get(
                employee=employee, questionnaire_id=questionnaire_id)

            if threshold.threshold_type == 'min' and threshold.min_value and answer_value < threshold.min_value:
                send_notification(employee, questionnaire_id,
                                  'Value below minimum threshold')
            elif threshold.threshold_type == 'max' and threshold.max_value and answer_value > threshold.max_value:
                send_notification(employee, questionnaire_id,
                                  'Value exceeds maximum threshold')
            elif threshold.threshold_type == 'exact' and threshold.exact_value and answer_value != threshold.exact_value:
                send_notification(employee, questionnaire_id,
                                  'Value does not match exact threshold')
        except Threshold.DoesNotExist:
            pass  # しきい値が設定されていない場合は何もしない

        return redirect('daily_report_list')


def show_notifications(request):
    # 現在ログインしている管理者の通知を取得
    notifications = Notification.objects.filter(
        employee=request.user.employee, is_read=False).order_by('-created_at')

    return render(request, 'myapp/notifications.html', {'notifications': notifications})

# 既読処理のビュー


def mark_as_read(request, notification_id):
    try:
        # 指定された通知を取得
        notification = Notification.objects.get(id=notification_id)

        # 通知がログインしているユーザーのものであるか確認
        if notification.employee == request.user.employee:
            # 通知を既読に変更
            notification.is_read = True
            notification.save()

        return redirect('show_notifications')  # 通知一覧ページにリダイレクト
    except Notification.DoesNotExist:
        # 通知が見つからない場合
        return redirect('show_notifications')


# セッションの時間制限（例: 30分）
SESSION_TIMEOUT_MINUTES = 30

# ログインビュー


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # ユーザー認証
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # ログイン
                request.session['last_activity'] = timezone.now(
                ).timestamp()  # 最終アクセス時間をセッションに記録

                # ユーザーが従業員かどうかをチェックして遷移先を判別
                employee = Employee.objects.get(user=user)
                if employee.employee_type == 'admin':
                    return redirect('admin_dashboard')  # 管理者用ダッシュボードへリダイレクト
                else:
                    # アンケート回答者用ページへリダイレクト
                    return redirect('employee_dashboard')
            else:
                # 認証に失敗した場合の処理
                return render(request, 'myapp/login.html', {'form': form, 'error': '名前またはパスワードが間違っています。'})
    else:
        form = LoginForm()

    return render(request, 'myapp/login.html', {'form': form})

# 自動ログアウトのセッションタイムアウト処理


@login_required
def check_session_timeout(request):
    last_activity = request.session.get('last_activity', None)
    if last_activity:
        # 現在の時間と最終アクセス時間を比較してタイムアウトをチェック
        now = timezone.now().timestamp()
        elapsed_time = now - last_activity
        if elapsed_time > SESSION_TIMEOUT_MINUTES * 60:
            logout(request)  # セッションが時間制限を超えたらログアウト
            return redirect('login_view')  # ログイン画面にリダイレクト
        else:
            # セッションが有効なら、最終アクセス時間を更新
            request.session['last_activity'] = now

    # ユーザーがどちらのページにいるか判別
    employee = Employee.objects.get(user=request.user)
    if employee.employee_type == 'admin':
        return redirect('admin_dashboard')
    else:
        return redirect('employee_dashboard')


@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


@login_required
def employee_dashboard(request):
    return render(request, 'employee_dashboard.html')
