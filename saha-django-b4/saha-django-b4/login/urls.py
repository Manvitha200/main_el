from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),  # Registration endpoint
        path("login/", views.login_user, name="login_user"),

]
