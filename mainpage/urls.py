from django.urls import path
from mainpage import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('task/list/', views.task_board_page, name='task_board_page'),
    path('task/<int:pk>/', views.task_detail, name="task_detail"),
    path('task/new/', views.task_new, name='task_new'),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout')
]
