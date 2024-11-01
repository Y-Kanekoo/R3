# myapp/views.py
from .models import Employee
from rest_framework import generics
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from .models import Employee, Questionnaire, DailyReport, DailyReportAnswer, QuestionnaireThreshold, QuestionnaireOption
from .serializers import EmployeesSerializer, QuestionnairesSerializer, DailyReportsSerializer, DailyReportAnswersSerializer
import requests
from django.contrib import messages
from .forms import EmployeeForm
from django.db.models import Q


class EmployeesList(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeesSerializer

# # APIからデータを取得し、テンプレートに表示するためのビュー


def show_employees(request):
    # ローカルサーバー上のAPIエンドポイントからデータを取得
    response = requests.get('http://127.0.0.1:8000/api/EmployeesList/')
    employees = response.json()  # APIから取得したデータをJSON形式で読み込む
    return render(request, 'myapp/show_employees.html', {'employees': employees})


def employee_management(request, employee_id=None):
    # ソート用のパラメータを取得
    sort_by = request.GET.get('sort', 'name')  # デフォルトは名前でソート
    direction = request.GET.get('direction', 'asc')  # デフォルトは昇順

    # ソート条件の設定
    if direction == 'desc':
        sort_by = f'-{sort_by}'

    # 従業員一覧の取得（ソート適用）
    employees = Employee.objects.all().order_by(sort_by)

    # 編集対象の従業員取得
    employee = get_object_or_404(
        Employee, id=employee_id) if employee_id else None

    if request.method == 'POST':
        if 'delete' in request.POST:
            if employee:
                employee.delete()
                messages.success(request, f'{employee.name}さんを削除しました。')
                return redirect('employee_management')
        else:
            # 追加・編集の処理
            name = request.POST.get('name')
            employee_type = request.POST.get('employee_type')

            if not name:
                messages.error(request, '名前を入力してください。')
            else:
                # 重複チェック
                duplicate = Employee.objects.filter(
                    Q(name=name) &
                    Q(employee_type=employee_type)
                ).exclude(id=employee_id).exists()

                if duplicate:
                    messages.error(request, 'この名前とタイプの組み合わせは既に存在します。')
                else:
                    if employee:
                        # 更新
                        employee.name = name
                        employee.employee_type = employee_type
                        employee.save()
                        messages.success(request, f'{name}さんの情報を更新しました。')
                    else:
                        # 新規作成
                        Employee.objects.create(
                            name=name, employee_type=employee_type)
                        messages.success(request, f'{name}さんを追加しました。')
                    return redirect('employee_management')

    # テンプレートに渡すコンテキスト
    context = {
        'employees': employees,
        'editing_employee': employee,
        'employee_types': Employee.EMPLOYEE_TYPE_CHOICES,
        'current_sort': sort_by.replace('-', ''),
        'current_direction': direction,
    }

    return render(request, 'myapp/employee_management.html', context)


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
    threshold_dict = {threshold.questionnaire_id: (
        threshold.threshold_min, threshold.threshold_max) for threshold in thresholds}

    # レポートごとに回答を整理
    report_data = []
    for report in reports:
        report_answers = []
        for answer in answers:
            if answer.daily_report_id == report.id:
                # 閾値を取得
                min_threshold, max_threshold = threshold_dict.get(
                    answer.questionnaire.id, (None, None))

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
                    answer_text = option_dict.get(
                        (answer.questionnaire.id, ansewer_value), answer.answer)
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

    # アンケートと選択肢データを取得
    questionnaires = Questionnaire.objects.all()
    options = QuestionnaireOption.objects.all()
    # コンテキストにデータを渡す
    context = {
        'questionnaires': questionnaires,
        'options': options,

    }

    return render(request, 'myapp/submit_answers.html', context)

    # def submit_answers(request):
    # if request.method == 'POST':
    #     # フォームから送信されたemployee_idを取得し、該当する社員を取得
    #     employee_id = request.POST.get('employee_id')
    #     employee = get_object_or_404(Employee, id=employee_id)

    #     # レポートタイプを指定（ここでは仮に'morning'）
    #     report_type = 'morning'

    #     # DailyReportを作成
    #     daily_report = DailyReport.objects.create(
    #         employee=employee,
    #         report_datetime=timezone.now(),
    #         report_type=report_type
    #     )

    #     # 各質問の回答を処理し、DailyReportAnswerモデルに保存
    #     questionnaires = Questionnaire.objects.filter(type='morning')  # morningタイプの質問を取得
    #     for questionnaire in questionnaires:
    #         # フォームから選択された回答を取得
    #         answer_value = request.POST.get(f'questionnaire_{questionnaire.id}')
    #         if answer_value:  # 選択肢がある場合
    #             # 閾値を計算するために必要なロジックを追加することもできます
    #             threshold_value = 0  # ここではデフォルト値を設定しています。必要に応じて計算を実装してください。

    #             DailyReportAnswer.objects.create(
    #                 daily_report=daily_report,
    #                 questionnaire=questionnaire,
    #                 answer=answer_value,
    #                 threshold_value=threshold_value
    #             )

    #     # データを保存した後にリダイレクトすることを検討してください
    #     return redirect('some_view_name')  # 適切なリダイレクト先を指定

    # # アンケートと選択肢データを取得
    # questionnaires = Questionnaire.objects.filter(type='morning')  # morningタイプの質問を取得
    # options = QuestionnaireOption.objects.all()

    # # コンテキストにデータを渡す
    # context = {
    #     'questionnaires': questionnaires,
    #     'options': options,
    # }

    # return render(request, 'myapp/submit_answers.html', context)
