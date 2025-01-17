# login/models.py
from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email_id = models.EmailField(unique=True)
    password_hashed = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    skills = models.TextField(blank=True, null=True)
    preferences = models.TextField(blank=True, null=True)
    last_login = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
