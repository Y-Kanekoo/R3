from django import forms
from .models import Employee


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

# class ThresholdForm(forms.ModelForm):
#     class Meta:
#         model = Threshold
#         fields = ['employee', 'questionnaire', 'min_value',
#                   'max_value', 'exact_value', 'threshold_type']
#         widgets = {
#             'threshold_type': forms.Select(choices=Threshold.THRESHOLD_TYPE_CHOICES),
#         }


# # ログインフォーム
# class LoginForm(forms.Form):
#     username = forms.CharField(
#         label="名前",
#         max_length=255,
#         widget=forms.TextInput(attrs={'autocomplete': 'on'})  # オートコンプリートを有効にする
#     )
#     password = forms.CharField(
#         label="パスワード",
#         widget=forms.PasswordInput(
#             attrs={'autocomplete': 'on'})  # パスワード入力用フィールド
#     )
