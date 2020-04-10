from django.urls import path
from mainpage import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('task/list/', views.task_board_page, name='task_board_page'),
    path('task/list/user-set/', views.task_board_set, name='task_board_set'),
    path('task/list/user-performs/', views.task_board_performs, name='task_board_performs'),
    path('task/new/', views.task_new, name='task_new'),
    path('task/<int:pk>/', views.task_detail, name="task_detail"),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:pk>/accept/', views.accept_task, name='accept_task'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout')
]
