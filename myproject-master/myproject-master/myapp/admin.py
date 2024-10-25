# from django.contrib import admin
# from .models import Employee, Questionnaire, DailyReport, DailyReportAnswer, Threshold

# # Employeeモデルの管理画面設定


# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'employee', 'create_at')
#     search_fields = ('name')
#     list_filter = ('employee_type')

# # Questionnaireモデルの管理画面設定,日報のアンケートリスト


# class QuestionnaireAdmin(admin.ModelAdmin):
#     list_display = ('title', 'type', 'created_at')
#     search_fields = ('title',)
#     list_filter = ('type',)

# # DailyReportモデルの管理画面設定,日報リスト


# class DailyReportAdmin(admin.ModelAdmin):
#     list_display = ('employee', 'report_datetime', 'report_type')
#     list_filter = ('report_type',)

# # DailyReportAnswerモデルの管理画面設定,日報の回答リスト


# class DailyReportAnswerAdmin(admin.ModelAdmin):
#     list_display = ('daily_report', 'questionnaire', 'answer')

# # Thresholdモデルの管理画面設定


# class ThresholdAdmin(admin.ModelAdmin):
#     list_display = ('questionnaire', 'min_value', 'max_value', 'exact_value')
#     list_filter = ('threshold_type',)


# # 管理画面にモデルを登録する
# admin.site.register(Employee)  # Employeeモデルを管理画面に登録
# admin.site.register(Questionnaire)  # Questionnaireモデルを管理画面に登録
# admin.site.register(DailyReport)  # DailyReportモデルを管理画面に登録
# admin.site.register(DailyReportAnswer)  # DailyReportAnswerモデルを管理画面に登録
# admin.site.register(Threshold)  # Thresholdモデルを管理画面に登録
