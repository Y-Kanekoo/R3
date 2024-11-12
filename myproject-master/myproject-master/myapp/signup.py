from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label="ユーザー名",
        widget=forms.TextInput(attrs={
            "placeholder": "ユーザー名を入力",
            "class": "form-control"
        })
    )
    email = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(attrs={
            "placeholder": "example@example.com",
            "class": "form-control"
        })
    )
    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={
            "placeholder": "パスワードを入力",
            "class": "form-control"
        })
    )
    password2 = forms.CharField(
        label="パスワード確認",
        widget=forms.PasswordInput(attrs={
            "placeholder": "もう一度パスワードを入力",
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
