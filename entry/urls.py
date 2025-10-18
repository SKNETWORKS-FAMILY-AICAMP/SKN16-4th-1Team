from django.urls import path
from . import views

urlpatterns = [
    path('', views.entry, name='entry'),
    path('show', views.show, name='show'),
    path('show/<int:diary_id>', views.detail, name='detail'),
    path('productivity/', views.productivity, name='productivity'),
    path('generate-image/<int:diary_id>/', views.generate_image, name='generate_image'),
    path('save-image/<int:diary_id>/', views.save_image, name='save_image'),

    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/settings/', views.settings_view, name='settings'),
    
    path('api/diary/dates/', views.get_diary_dates, name='get_diary_dates'),
    path('api/diary/<str:date_str>/', views.get_diary_by_date, name='get_diary_by_date'),
<<<<<<< HEAD
=======
    
>>>>>>> hyunmin
]