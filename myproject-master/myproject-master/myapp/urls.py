# myapp/urls.py
from django.urls import path
from .views import EmployeesList, show_employees, QuestionnairesList, show_questionnaires, Daily_reportsList, show_daily_reports, Daily_report_answersList, show_report_answers, ThresholdsList, show_thresholds, show_notifications, mark_as_read, login_view, check_session_timeout, admin_dashboard, employee_dashboard


urlpatterns = [

    path('api/EmployeesList/', EmployeesList.as_view(), name='Employees_List'),
    path('show_employees/', show_employees, name='show_employees'),


    path('api/QuestionnairesList/', QuestionnairesList.as_view(),
         name='Questionnaires_List'),  # 日報のアンケートリスト
    path('show_questionnaires/', show_questionnaires, name='show_questionnaires'),

    path('api/Daily_reportsList/', Daily_reportsList.as_view(),
         name='Daily_reports_List'),  # 日報リスト
    path('show_daily_reports/', show_daily_reports, name='show_daily_reports'),


    path('api/Daily_report_answersList/', Daily_report_answersList.as_view(),
         name='Daily_report_answers_List'),  # 日報の回答リスト
    path('show_report_answers/', show_report_answers, name='show_report_answers'),


    path('api/ThresholdsList/', ThresholdsList.as_view(),
         name='Thresholds_List'),  # 閾値を設定
    path('show_thresholds/', show_thresholds, name='show_threshold'),

    # 通知の表示
    path('notifications/', show_notifications, name='show_notifications'),

    # 通知の既読処理
    path('notifications/mark_as_read/<int:notification_id>/',
         mark_as_read, name='mark_as_read'),

    # ログイン
    path('login/', login_view, name='login_view'),  # ログインページ
    path('check_session/', check_session_timeout,
         name='check_session_timeout'),  # セッションチェック用

]

urlpatterns += [
    path('admin_dashboard/', admin_dashboard,
         name='admin_dashboard'),  # 管理者用ダッシュボード
    path('employee_dashboard/', employee_dashboard,
         name='employee_dashboard'),  # アンケート回答者用ページ
]
