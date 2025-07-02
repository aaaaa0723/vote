from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import BootstrapAuthenticationForm

app_name = 'voteapp'

urlpatterns = [
    path('', views.index, name='index'),  # 首頁
    path('voting/', views.voting, name='voting'),  # 投票頁面
    path('vote/', views.vote_all, name='vote_all'),  # 處理投票送出
    path('result/', views.result, name='result'),
    path('login/', auth_views.LoginView.as_view(template_name='voteapp/login.html', authentication_form=BootstrapAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='voteapp:index'), name='logout'),
]
