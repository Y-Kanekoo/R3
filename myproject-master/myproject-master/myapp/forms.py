from django import forms
from .models import DailyReportAnswer

class DailyReportAnswerForm(forms.ModelForm):
    class Meta:
        model = DailyReportAnswer
        fields = ['questionnaire', 'answer']
        widgets = {
            'questionnaire': forms.HiddenInput(),  # 質問を隠しフィールドにする場合
            'answer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '回答を入力してください'}),
        }
        labels = {
            'answer': '回答',
        }

