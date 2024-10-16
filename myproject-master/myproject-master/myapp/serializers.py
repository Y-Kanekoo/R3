# myapp/serializers.py
from rest_framework import serializers
from .models import Employee, Questionnaire, DailyReport, DailyReportAnswer

class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'  # 全てのフィールドをシリアライズ   

class QuestionnairesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = '__all__'  # 全てのフィールドをシリアライズ   

class DailyReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReport
        fields = '__all__'  # 全てのフィールドをシリアライズ   

class DailyReportAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReportAnswer
        fields = '__all__'  # 全てのフィールドをシリアライズ   