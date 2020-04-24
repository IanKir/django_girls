"""Модуль для работы с роутингом запросов клиента."""
from django.urls import path
from core import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('task/list/', views.task_board_page, name='task_board_page'),
    path('task/list/user-set/', views.task_board_set, name='task_board_set'),
    path(
        'task/list/user-performs/',
        views.task_board_performs,
        name='task_board_performs',
    ),
    path('task/new/', views.task_new, name='task_new'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:pk>/accept/', views.accept_task, name='accept_task'),
    path('user-sign-in/', views.sign_in_user, name='sign_in_user'),
    path('user-sign-up/', views.sign_up_user, name='sign_up_user'),
    path('user-logout/', views.user_logout, name='user_logout'),
]
