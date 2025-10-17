from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.entry, name='entry'),
    path('login/', auth_views.LoginView.as_view(
        template_name='entry/login.html',
        authentication_form=LoginForm,
        redirect_authenticated_user=True,
        extra_context={'title': '로그인', 'subtitle': '일기를 작성하려면 로그인하세요.'},
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='entry'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('show', views.show, name='show'),
    path('show/<int:diary_id>', views.detail, name='detail'),
    path('productivity/', views.productivity, name='productivity'),
    path('generate-image/<int:diary_id>/', views.generate_image, name='generate_image'),
    path('finalize-image/<int:diary_id>/', views.finalize_image, name='finalize_image'),
]
