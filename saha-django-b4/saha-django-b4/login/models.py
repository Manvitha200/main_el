from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, default="Employee")
    skills = models.TextField(blank=True)
    preferences = models.TextField(blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Login(models.Model):
    email = models.EmailField(unique=True)  # Email as unique identifier
    password_hashed = models.CharField(max_length=255)  # Store hashed passwords
    last_login = models.DateTimeField(auto_now=True)  # Automatically updated on login

    def __str__(self):
        return self.email