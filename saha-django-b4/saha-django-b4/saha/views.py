# from django.shortcuts import render, redirect



# def home(request):
#     # You can render a homepage template or redirect to login/signup
#     return redirect('login')  # Redirect to login page (or a homepage if you prefer)



# from django.shortcuts import render

# def login(request):
#     return render(request, 'login/login.html')  # Render the login template


from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect


# Signup view
def signup(request):
    return HttpResponse("This is the signup page.")

# Login view
def login(request):
    return HttpResponse("This is the login page.")



# Logout view
def logout(request):
    auth_logout(request)  # Logs out the user
    return redirect('/')  
