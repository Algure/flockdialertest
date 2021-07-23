from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView,RetrieveUpdateDestroyAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from django.http import HttpResponse
from django.http import Http404

from dialerapp.models import User
from dialerapp.models import Company
from dialerapp.serializers import UserSerializer
from dialerapp.serializers import CompanySerializer


def login(request):
    try:
        user_email = str(request.query_params.get('user_email', None))
        password = str(request.query_params.get('user_pass', None))
        if user_email is None or password is None :
            raise ValueError({ 'invalid input.' })

        user_object_collection = User.objects.filter(email = user_email).values_list()
        if len(user_object_collection) <= 0:
             raise ValidationError({ 'User does not exist' })

        stored_password = str(user_object_collection[0]['password']);
        if stored_password != password:
            raise ValidationError({ 'Password does not match' })

        return UserSerializer(user_object_collection[0]).to_representation()
    except ValueError:
        raise ValidationError({ 'user_email': 'A valid input is required' , 'user_pass' : 'A valid input is required'})

class DataPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id', 'company_id','name')
    search_fields = ('name', 'company_name')
    pagination_class = DataPagination

class UserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializer

class UserCreate(CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            user_phone = request.data.get('phone')
            user_email = request.data.get('email')
            queryset = User.objects.filter(phone = user_phone)
            queryset2 = User.objects.filter(email = user_email)
            assert((str(user_phone)).startswith('+')) # User phone number must start with +
            if user_phone is None or len(queryset.values_list()) > 0:
                raise ValidationError({ 'user phone number exists' })
            elif len(queryset2.values_list()) > 0:
                 raise ValidationError({ 'user email exists' })
        except ValueError:
            raise ValidationError({ 'user_phone': 'A valid number is required' })
        return super().create(request, *args, **kwargs)


class CompanyList(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id', 'name', 'phone')
    search_fields = ('name')
    pagination_class = DataPagination

class CompanyRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    lookup_field = 'id'
    serializer_class = CompanySerializer

class CompanyCreate(CreateAPIView):
    serializer_class = CompanySerializer

    def create(self, request, *args, **kwargs):
            try:
                company_phone = request.data.get('phone')
                queryset = Company.objects.filter(phone = company_phone)
                assert((str(company_phone)).startswith('+')) # Company phone number must start with +
                
                if company_phone is None or len(queryset.values_list()) > 0:
                    raise ValidationError({ 'Company phone number already exists' })
            except ValueError:
                raise ValidationError({ 'company_phone': 'A valid number is required' })
            return super().create(request, *args, **kwargs)