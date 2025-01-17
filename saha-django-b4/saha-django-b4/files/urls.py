
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_project_files, name='list_project_files'),
    path('upload/', views.upload_project_file, name='upload_project_file'),
    path('download/<str:file_id>/', views.download_project_file, name='download_project_file'),
]
