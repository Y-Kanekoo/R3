# forms.py

from django import forms
from .models import Employee, Questionnaire


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'employee_type']
        labels = {
            'name': '従業員の名前',
            'employee_type': '従業員のタイプ(管理者/一般)',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '名前を入力'}),
            'employee_type': forms.Select(attrs={'class': 'form-select'}),
        }

# アンケートデータの入力フォーム
class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ['title', 'type', 'answer_type']