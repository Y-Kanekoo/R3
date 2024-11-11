# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.contrib.auth import login, get_user_model,authenticate
from .models import Employee, Questionnaire, DailyReport, DailyReportAnswer, QuestionnaireThreshold, QuestionnaireOption
from .serializers import EmployeesSerializer, QuestionnairesSerializer, DailyReportsSerializer, DailyReportAnswersSerializer
from django.utils import timezone
import requests
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import EmployeeForm, QuestionnaireForm
from django.db.models import Q
from django.urls import reverse_lazy,reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.hashers import check_password 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import generics  # 外部ライブラリのインポート
from myapp.signup import SignUpForm  # 最後にアプリ関連のインポートを行う


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
    questionnaires = response.json() if response.status_code == 200 else []
    return render(request, 'myapp/show_questionnaires.html', {'questionnaires': questionnaires})

class Daily_report_answersList(generics.ListAPIView):
    queryset = DailyReportAnswer.objects.all()
    serializer_class = DailyReportAnswersSerializer

def show_report_answers(request):
    response = requests.get('http://127.0.0.1:8000/api/Daily_report_answersList/')
    answers = response.json() if response.status_code == 200 else []
    return render(request, 'myapp/show_report_answers.html', {'answers': answers})

class Daily_reportsList(generics.ListAPIView):
    queryset = DailyReport.objects.all()
    serializer_class = DailyReportsSerializer

def show_daily_reports(request):
    # レポートを取得
    reports = DailyReport.objects.select_related('employee').all()
    # 質問を取得
    questionnaires = Questionnaire.objects.all().order_by('id')
    # 回答を取得して質問の順にソート
    answers = DailyReportAnswer.objects.select_related('questionnaire').order_by('questionnaire__id')
    # 質問の選択肢を取得して辞書に整理
    options = QuestionnaireOption.objects.all()
    option_dict = {
        (option.questionnaire_id, option.option_value): option.option_text
        for option in options
    }

    # 閾値データを取得して辞書に整理
    thresholds = QuestionnaireThreshold.objects.all()
    threshold_dict = {threshold.questionnaire_id: (threshold.threshold_min, threshold.threshold_max) for threshold in thresholds}

    # レポートごとに回答を整理
    report_data = []
    for report in reports:
        report_answers = []
        for answer in answers:
            if answer.daily_report_id == report.id:
                # 閾値を取得
                min_threshold, max_threshold = threshold_dict.get(answer.questionnaire.id, (None, None))

                # 閾値を超えているかを判定
                threshold_exceeded = False
                if min_threshold is not None and max_threshold is not None:
                    try:
                        # 数値が入力された場合の比較
                        answer_value = float(answer.answer)
                        if not (min_threshold <= answer_value <= max_threshold):
                            threshold_exceeded = True
                    except ValueError:
                        # 数値でない場合は閾値判定をスキップ
                        pass

                # # 回答を選択肢のテキストに変換
                try:
                    ansewer_value = int(answer.answer)
                    answer_text = option_dict.get((answer.questionnaire.id, ansewer_value), answer.answer)
                except ValueError:
                    answer_text = answer.answer

                report_answers.append({
                    'question': answer.questionnaire.title,
                    'answer': answer_text,
                    'threshold_exceeded': threshold_exceeded  # 閾値超過のフラグを追加
                })
        

        report_data.append({
            'id': report.id,
            'employee': report.employee.name,
            'report_datetime': report.report_datetime,
            'report_type': report.report_type,
            'created_at': report.created_at,
            'updated_at': report.updated_at,
            'answers': report_answers
        })

    return render(request, 'myapp/show_daily_reports.html', {
        'reports': report_data,
        'questionnaires': questionnaires, 
    })


# 修正後のsubmit_answers関数
def submit_answers(request):
    if request.method == 'POST':
        # フォームから送信されたemployee_idを取得し、該当する社員を取得
        employee_id = request.POST.get('employee_id')
        employee = get_object_or_404(Employee, id=employee_id)

        # レポートタイプを指定（ここでは仮に'morning'）
        report_type = 'morning'

        # DailyReportを作成
        daily_report = DailyReport.objects.create(
            employee=employee,
            report_datetime=timezone.now(),
            report_type=report_type
        )

        # フォームからの回答を保存
        for key in request.POST:
            if key.startswith('questionnaire_'):  # 質問の回答のキーを確認
                questionnaire_id = int(key.split('_')[1])  # 質問IDを取得
                answer_value = request.POST[key]  # 回答を取得

                # DailyReportAnswerを作成 (threshold_valueを使用せずに)
                DailyReportAnswer.objects.create(
                    daily_report=daily_report,
                    questionnaire_id=questionnaire_id,
                    answer=answer_value,
                )

        # 回答が保存された後、日報の表示ページにリダイレクト
        return redirect('show_daily_reports')

    # GET リクエストの場合、質問と選択肢を取得
    questionnaires = Questionnaire.objects.all()
    options = QuestionnaireOption.objects.all()

    # コンテキストにデータを渡す
    context = {
        'questionnaires': questionnaires,
        'options': options,
    }

    return render(request, 'myapp/submit_answers.html', context)

#login
class CustomLoginView(LoginView):
    template_name = 'myapp/login.html'
    authentication_form = AuthenticationForm  # 認証フォームを指定
    redirect_authenticated_user = True  # ログイン済みユーザーはリダイレクトされる
    # `remember me`オプションを追加したい場合、セッションを拡張するためにオプション設定を追加
    def get_success_url(self):
        return reverse_lazy('myapp:home') 
class CustomLogoutView(LogoutView):
     def get_next_page(self):
        return reverse_lazy('myapp:login')

#ホーム画面
def home(request):
    return render(request, 'myapp/home.html')
 #signup
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("home")
    template_name = "myapp/signup.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return redirect(self.get_success_url())

User = get_user_model()
#プロフィール編集
def profile(request):
    if request.method == "POST":
        user = request.user
        user.email = request.POST["email"]
        user.username = request.POST["username"]
        user.save()
        return redirect("profile")
    else:
        return render(request, "myapp/profile.html")

# アンケート一覧表示ビュー
def questionnaire_list(request):
    # すべてのアンケートを取得
    questionnaires = Questionnaire.objects.all()
    return render(request, 'myapp/questionnaire_list.html', {'questionnaires': questionnaires})

# 新しいアンケートを作成するビュー
def questionnaire_create(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            # フォームが有効な場合、アンケートを保存
            form.save()
            messages.success(request, "アンケートが作成されました。")
            return redirect('myapp:questionnaire_list')
    else:
        form = QuestionnaireForm()
    return render(request, 'myapp/questionnaire_form.html', {'form': form})

# 既存のアンケートを編集するビュー
def questionnaire_update(request, pk):
    # 編集対象のアンケートを取得
    questionnaire = get_object_or_404(Questionnaire, pk=pk)
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST, instance=questionnaire)
        if form.is_valid():
            # フォームが有効な場合、変更内容を保存
            form.save()
            messages.success(request, "アンケートが更新されました。")
            return redirect('myapp:questionnaire_list')
    else:
        form = QuestionnaireForm(instance=questionnaire)
    return render(request, 'myapp/questionnaire_form.html', {'form': form})

# アンケートを削除するビュー
def questionnaire_delete(request, pk):
    # 指定されたアンケートが存在するか確認
    questionnaire = Questionnaire.objects.filter(pk=pk).first()
    if questionnaire:
        questionnaire.delete()
        messages.success(request, "アンケートが削除されました。")  # 削除成功メッセージ
    else:
        messages.error(request, "指定されたアンケートは存在しません。")  # エラーメッセージ
    # 一覧画面にリダイレクト
    return redirect('myapp:questionnaire_list')



# ユーザーリストの表示と権限の更新を行うビュー
@user_passes_test(lambda u: u.is_authenticated and u.employee_type == 'admin')
def user_list(request):
    user_data = Employee.objects.select_related('user').all()  # EmployeeとUserを関連付けて取得
    return render(request, 'myapp/user_list.html', {'user_data': user_data})
@user_passes_test(lambda u: u.is_authenticated and u.employee_type == 'admin')
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    employee = get_object_or_404(Employee, user=user)

    if request.method == 'POST':
        # POSTデータから  `is_superuser` の値を取得
        is_superuser = request.POST.get('is_superuser') == 'on'
        is_staff = request.POST.get('is_staff') == 'on'

        # UserとEmployeeの`is_staff`と`is_superuser`を更新
        user.is_superuser = is_superuser
        user.is_staff = is_superuser  # is_superuserがTrueならis_staffもTrueに
        user.employee_type = 'admin' if is_superuser else 'general'  # is_superuserがTrueならemployee_typeをadminに
        user.save()

        employee.is_superuser = is_superuser
        employee.is_staff = is_superuser  # is_superuserがTrueならis_staffもTrueに
        employee.employee_type = 'admin' if is_superuser else 'general'  # is_superuserがTrueならemployee_typeをadminに
        employee.save()

        user = get_object_or_404(User, id=user_id)
        employee = get_object_or_404(Employee, user=user)

        return redirect('myapp:user_list')  # 更新後にユーザーリストにリダイレクト

    return render(request, 'myapp:update_user.html', {'user': user, 'employee': employee})