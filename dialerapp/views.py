from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse
from django.http import Http404

from .models import User

from dialerapp.serializers import UserSerializer
from dialerapp.serializers import CompanySerializer

@csrf_exempt 
def change_password(request):
    try:
        user_email = str(request.data.get('user_email', None))
        user_password = str(request.data.get('user_pass', None))
        password_change =  str(request.query_params.get('user_pass_change', None))

        if user_email is None or user_password is None or password_change is None:
            raise ValueError({ 'invalid input.' })

        user_object_collection = User.objects.filter(email = user_email).values_list()
        if len(user_object_collection) <= 0:
             raise ValidationError({ 'User does not exist' })

        stored_password = str(user_object_collection[0]['password']);
        if stored_password != user_password:
            raise ValidationError({ 'Password does not match' })

        user_object = User.objects.get(email = user_email)
        user_object.password = password_change
        user_object.save()
        
        return UserSerializer(user_object_collection[0]).to_representation()
    except ValueError:
        raise ValidationError({ 'user_email': 'A valid input is required' , 'user_pass' : 'A valid input is required'})
 
@csrf_exempt 
def login(request):
    try:
        user_email = str(request.data.get('user_email', None))
        password = str(request.data.get('user_pass', None))
        if user_email is None or password is None :
            raise ValueError({ 'invalid input.' })

        print('email:  ' + user_email + '  password:  ' + password)
        user_object_collection = User.objects.get(email = user_email)
        if user_object_collection is None:
             raise ValidationError({ 'User does not exist' })

        stored_password = user_object_collection.password
        if stored_password != password:
            raise ValidationError({ 'Password does not match' })
        
        return UserSerializer(user_object_collection[0]).to_representation()
    except ValueError:
        raise ValidationError({ 'user_email': 'A valid input is required' , 'user_pass' : 'A valid input is required'})
