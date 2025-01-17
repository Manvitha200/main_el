from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_projects, name='projects_list'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('profile/', views.user_profile, name='user_profile'),
]
