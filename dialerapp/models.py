from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    company_id = models.CharField(max_length=50)
    company_name = models.CharField(max_length = 100)
    session_duration = models.CharField(max_length=50)

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    playlist = models.TextField()
    
