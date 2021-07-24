from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse
from django.http import Http404

from .models import User

