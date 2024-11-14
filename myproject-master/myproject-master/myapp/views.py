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
from django.utils.dateparse import parse_datetime
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test,login_required
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
import csv
from django.http import HttpResponse

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
    answers = DailyReportAnswer.objects.select_related(
        'questionnaire').order_by('questionnaire__id')

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

                # 回答を選択肢のテキストに変換
                try:
                    answer_value = int(answer.answer)
                    answer_text = option_dict.get((answer.questionnaire.id, answer_value), answer.answer)
                except ValueError:
                    answer_text = answer.answer

                report_answers.append({
                    'question': answer.questionnaire.title,
                    'answer': answer_text,  # テキストに変換された選択肢
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

@login_required
def submit_answers(request):
    if request.method == 'POST':
        # 現在のページ番号を取得
        page = int(request.POST.get('page', 1))

        # 最初のページで従業員IDを取得して処理
        if page == 1:
            # ログインしているユーザーの従業員IDを取得
            employee = request.user.employee  # ユーザーが従業員情報に関連付けられている前提
            employee_id = employee.id

            # DailyReportを作成
            report_type = 'morning'
            daily_report = DailyReport.objects.create(
                employee=employee,
                report_datetime=timezone.now(),
                report_type=report_type
            )

            # DailyReport IDをセッションに保存
            request.session['daily_report_id'] = daily_report.id
        else:
            # セッションからレポートIDを取得
            daily_report_id = request.session.get('daily_report_id')
            daily_report = get_object_or_404(DailyReport, id=daily_report_id)

        # 回答の保存
        for key, value in request.POST.items():
            if key.startswith('questionnaire_'):
                questionnaire_id = int(key.split('_')[1])
                DailyReportAnswer.objects.create(
                    daily_report=daily_report,
                    questionnaire_id=questionnaire_id,
                    answer=value
                )

        # 次のページへ
        if 'next' in request.POST:
            page += 1
        elif 'submit' in request.POST:
            return redirect('myapp:home')  # 送信後にhomeページへリダイレクト

    else:
        page = 1  # 初期ページ

    # 質問の取得とページネーション設定
    questionnaires = Questionnaire.objects.all()
    paginator = Paginator(questionnaires, 5)  # 1ページに5問表示
    paginated_questions = paginator.get_page(page)

    # 選択肢の取得
    options = QuestionnaireOption.objects.all()

    # ログインしている従業員の情報をコンテキストに追加
    employee = request.user.employee
    employee_name = employee.name  # 従業員名を取得

    # 各質問に対する回答を取得
    answers = {}
    for questionnaire in questionnaires:
        answer = DailyReportAnswer.objects.filter(
            daily_report__employee=employee, 
            questionnaire=questionnaire
        ).first()
        if answer:
            answers[questionnaire.id] = answer.answer

    # コンテキストにデータを渡す
    context = {
        'questionnaires': paginated_questions,
        'options': options,
        'page': page,
        'total_pages': paginator.num_pages,
        'employee_id': employee.id,  # 従業員ID
        'employee_name': employee_name,  # 従業員名
        'answers': answers  # 各質問の回答
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
@login_required
def home(request):
    # ログインユーザーに関連する Employee を取得
    employee = Employee.objects.get(user=request.user)

    # 最新のレポートを1つだけ取得
    latest_report = DailyReport.objects.filter(employee=employee).order_by('-report_datetime').first()

    if latest_report:
        # 最新のレポートに関連する回答を取得
        answers = DailyReportAnswer.objects.filter(daily_report=latest_report).select_related('questionnaire').order_by('questionnaire__id')

        # 質問の選択肢を取得して辞書に整理
        options = QuestionnaireOption.objects.all()
        option_dict = {
            (option.questionnaire_id, option.option_value): option.option_text
            for option in options
        }

        # 回答を選択肢のテキストに変換
        report_answers = []
        for answer in answers:
            try:
                answer_value = int(answer.answer)
                answer_text = option_dict.get((answer.questionnaire.id, answer_value), answer.answer)
            except ValueError:
                answer_text = answer.answer

            report_answers.append({
                'question': answer.questionnaire.title,
                'answer': answer_text,
            })

        report_data = {
            'id': latest_report.id,
            'employee': latest_report.employee.name,
            'report_datetime': latest_report.report_datetime,
            'report_type': latest_report.report_type,
            'created_at': latest_report.created_at,
            'updated_at': latest_report.updated_at,
            'answers': report_answers
        }

    else:
        report_data = None

    # home.html にデータを渡す
    return render(request, 'myapp/home.html', {
        'report': report_data,
    })

#自身の回答データ確認view
def show_own_answer(request):
    # ログインユーザーに関連する Employee を取得
    employee = Employee.objects.get(user=request.user)

    # デフォルトで全てのレポートと回答を取得
    reports = DailyReport.objects.filter(employee=employee).select_related('employee')
    answers = DailyReportAnswer.objects.filter(daily_report__employee=employee).select_related('questionnaire').order_by('questionnaire__id')

    # 検索条件（日付とレポートタイプ）の取得
    search_date = request.GET.get('date', None)
    search_type = request.GET.get('type', None)

    # 日付によるフィルタリング
    if search_date:
        # 文字列を日付形式に変換してフィルタ
        date_obj = parse_datetime(search_date)
        reports = reports.filter(report_datetime__date=date_obj.date())

    # レポートタイプによるフィルタリング
    if search_type:
        reports = reports.filter(report_type=search_type)

    # 質問の選択肢を取得して辞書に整理
    options = QuestionnaireOption.objects.all()
    option_dict = {
        (option.questionnaire_id, option.option_value): option.option_text
        for option in options
    }

    # レポートごとに回答を整理
    report_data = []
    for report in reports:
        report_answers = []
        for answer in answers:
            if answer.daily_report_id == report.id:
                # 回答を選択肢のテキストに変換
                try:
                    answer_value = int(answer.answer)
                    answer_text = option_dict.get((answer.questionnaire.id, answer_value), answer.answer)
                except ValueError:
                    answer_text = answer.answer

                report_answers.append({
                    'question': answer.questionnaire.title,
                    'answer': answer_text,
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

    # show_own_answer.html にデータを渡す
    return render(request, 'myapp/show_own_answer.html', {
        'reports': report_data,
    })

 #signup
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("myapp:home")
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
        # フォームから送信されたデータを取得し、`user`オブジェクトに設定
        user.email = request.POST.get("email")  # emailの更新
        username = request.POST.get("username")  # usernameの更新
        
        # usernameが存在する場合にのみ更新
        if username:
            user.username = username
        
        # データベースに保存
        user.save()
        
        # 保存後にプロフィールページをリロード
        return redirect("myapp:profile")
    else:
        # 現在のユーザー情報をフォームに表示
        return render(request, "myapp/profile.html", {"user": request.user})



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
            # Save the Questionnaire instance
            questionnaire = form.save()

            # If the answer_type is 'select', handle the options
            if form.cleaned_data['answer_type'] == 'select':
                # Collect options from the form
                options_data = request.POST.getlist('option_value')  # Get option_value fields
                options_text = request.POST.getlist('option_text')   # Get option_text fields
                
                for value, text in zip(options_data, options_text):
                    # Save each option in QuestionnaireOption
                    QuestionnaireOption.objects.create(
                        questionnaire=questionnaire,
                        option_value=value.strip(),
                        option_text=text.strip()
                    )
            
            if form.cleaned_data['answer_type'] == 'text':
                text_response = request.POST.get('text_response')
            if form.cleaned_data['answer_type'] == 'time_field':
                time_response = request.POST.get('time_response')

            return redirect('myapp:questionnaire_list')  # Redirect to a success page after saving
    else:
        form = QuestionnaireForm()

    return render(request, 'myapp/questionnaire_form.html', {'form': form})

# アンケートを編集するビュー
def questionnaire_update(request, pk):
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
    questionnaire = Questionnaire.objects.filter(pk=pk).first()
    if questionnaire:
        questionnaire.delete()  # アンケートを削除
        messages.success(request, "アンケートが削除されました。")
    else:
        messages.error(request, "指定されたアンケートは存在しません。")
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


def export_reports_csv(request):
    response = HttpResponse(content_type='text/csv')
    
    # ファイル名を日本語にしたい場合は下記のようにコメントを使用して指定します。
    # response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'日報一覧.csv'
    response['Content-Disposition'] = 'attachment; filename="daily_reports.csv"'

    writer = csv.writer(response)

    # CSVのヘッダー行
    headers = ['レポートID', '従業員ID', 'レポート日時', 'レポートタイプ', '作成日時', '更新日時']
    for question in Questionnaire.objects.all():
        headers.append(question.title)
    writer.writerow(headers)

    # CSVのデータ行
    for report in DailyReport.objects.select_related('employee'):
        row = [
            report.id,
            report.employee.name,
            report.report_datetime,
            report.report_type,
            report.created_at,
            report.updated_at
        ]

        # 各質問の回答を取得
        for question in Questionnaire.objects.all():
            answer = DailyReportAnswer.objects.filter(
                daily_report=report, questionnaire=question
            ).first()
            answer_text = answer.answer if answer else ""
            row.append(answer_text)

        writer.writerow(row)

    # UTF-8 エンコーディングを使用（ファイルが壊れることなく保存されます）
    response.write('\ufeff'.encode('utf8'))
    return response