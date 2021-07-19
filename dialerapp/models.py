from django.db import models

class User(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    company_id = models.CharField(max_length=50)
    company_name = models.CharField(max_length = 100)
    session_duration = models.CharField(max_length=50)

class Company(models.Model):
    name = models.CharField(max_length=100)
    playlist = models.TextField()
    
