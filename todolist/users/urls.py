from django.urls import path
from . import views

urlpatterns = [
    path('settings', views.settings, name='settings'),
    path('edit-user/', views.edit_user, name='edit_user'),
    path('user/<int:user_id>/analytics/', views.user_analytics, name='user_analytics'),
    path('chart/filter/', views.filter_chart, name='filter_chart'),
    path('switch-theme/', views.switch_theme, name='switch_theme'),
    path('set-timezone/', views.set_timezone, name='set_timezone'),
]