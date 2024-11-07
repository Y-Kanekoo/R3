# myapp/urls.py
from django.urls import path
from .views import EmployeesList, show_employees, QuestionnairesList, show_questionnaires, Daily_reportsList, show_daily_reports, Daily_report_answersList, show_report_answers,submit_answers, submit_answers, CustomLoginView, CustomLogoutView, profile, questionnaire_list, questionnaire_create, questionnaire_update, questionnaire_delete
from . import views
from django.contrib.auth import views as auth_views

app_name = 'myapp' 

urlpatterns = [
    path('api/EmployeesList/', EmployeesList.as_view(), name='Employees_List'),
    path('show_employees/', show_employees, name='show_employees'),
    path('api/QuestionnairesList/', QuestionnairesList.as_view(), name='Questionnaires_List'),
    path('show_questionnaires/', show_questionnaires, name='show_questionnaires'),
    path('api/Daily_reportsList/', Daily_reportsList.as_view(), name='Daily_reports_List'),
    path('show_daily_reports/', show_daily_reports, name='show_daily_reports'),
    path('api/Daily_report_answersList/', Daily_report_answersList.as_view(), name='Daily_report_answers_List'),
    path('show_report_answers/', show_report_answers, name='show_report_answers'),
    path('submit_answers/', submit_answers, name='submit_answers'),
    path('show_employees/', views.show_employees, name='show_employees'), 
    
    path('questionnaires/', questionnaire_list, name='questionnaire_list'),
    path('questionnaires/create/', questionnaire_create, name='questionnaire_create'),
    path('questionnaires/update/<int:pk>/', questionnaire_update, name='questionnaire_update'),
    path('questionnaires/delete/<int:pk>/', questionnaire_delete, name='questionnaire_delete'),

    path('home/', views.home, name='home'),
    path("login/", CustomLoginView.as_view(), name="login"),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path("profile/", views.profile, name="profile"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
]
