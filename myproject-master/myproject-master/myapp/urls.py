from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.show_daily_reports, name='show_daily_reports'),
    # path('login/', views.login_view, name='login'),  # ログイン用URL
    # path('logout/', views.logout_view, name='logout'),  # ログアウト用のURL
]
