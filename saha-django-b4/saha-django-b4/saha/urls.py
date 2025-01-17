from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('login.urls')),  # Include URLs from the `login` app
    path('', lambda request: HttpResponse("Welcome to the Homepage!"), name='home'),
]
