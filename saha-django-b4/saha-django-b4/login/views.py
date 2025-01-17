from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Login



@api_view(['POST'])
def register_user(request):
    try:
        print("Received request data:", request.data)  # Debugging: Log received data

        # Validate required fields
        required_fields = ['user_id', 'name', 'email', 'password', 'role']
        missing_fields = [field for field in required_fields if field not in request.data or not request.data[field]]
        
        if missing_fields:
            print(f"Missing fields: {missing_fields}")  # Debugging: Print missing fields
            return Response({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Hash the password
        hashed_password = make_password(request.data['password'])

        # Inside the register_user view function
        print("Creating user with data:", request.data)  # Log the data being passed

        # Create and save the user
        user = User.objects.create(
            user_id=request.data['user_id'],
            name=request.data['name'],
            email=request.data['email'],
            password=hashed_password,  # Store hashed password in User
            role=request.data['role'],
            skills=request.data.get('skills', ''),
            preferences=request.data.get('preferences', ''),
            last_login=request.data.get('last_login', None),
        )

        # Now save the login credentials in the 'login' table
        login = Login.objects.create(
            email=request.data['email'],
            password_hashed=hashed_password,  # Store hashed password in Login
            last_login=request.data.get('last_login', None)
        )

        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"Error in register_user: {str(e)}")  # Debugging: Log the error message
        return Response({"error": f"An error occurred during registration: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate


from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
import json
from .models import Login

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"error": "Email and password are required."}, status=400)

            # Retrieve the user by email
            user = Login.objects.filter(email=email).first()

            if not user:
                return JsonResponse({"error": "Invalid email or password."}, status=401)

            # Debugging: Log data being compared
            print("Email from request:", email)
            print("Password from request:", password)
            print("Hashed password in database:", user.password_hashed)

            # Verify the password using Django's check_password method
            if check_password(password, user.password_hashed):
                return JsonResponse({"message": "Login successful."}, status=200)
            else:
                return JsonResponse({"error": "Invalid email or password."}, status=401)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
