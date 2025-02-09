from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('track/', views.track_period, name='track_period'),
    path('profile/', views.profile, name='profile'),  # Direct reference to views.profile
    path('log/',views.log_period,name ='log_period'),
    path('settings/', views.settings_view, name='settings'),
    path('new_log_period/', views.new, name='new'),
]

