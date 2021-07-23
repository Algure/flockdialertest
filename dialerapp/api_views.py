from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView,RetrieveUpdateDestroyAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse
from django.http import Http404

from dialerapp.models import User
from dialerapp.models import Company
from dialerapp.serializers import UserSerializer
from dialerapp.serializers import CompanySerializer

class UserChangePasswordView(GenericAPIView):

    def post(self, request, format=None, id=None):
        try:
            user_email = str(request.data.get('user_email', None))
            user_password = str(request.data.get('user_pass', None))
            user_phone = str(request.data.get('user_phone', None))
            password_change =  str(request.data.get('user_pass_change', None))

            if (user_email is None and user_phone is None) or user_password is None or password_change is None:
                raise ValueError({ 'invalid input.' })

            user_object = None
            if user_phone is not None:
                user_object = User.objects.get(phone = user_phone)
            elif user_email is not None:
                user_object = User.objects.get(email = user_email)

            if user_object is None:
                raise ValidationError({ 'User does not exist' })

            stored_password = user_object.password
            if stored_password != user_password:
                raise ValidationError({ 'Password does not match' })

            if stored_password == password_change:
                raise ValidationError({"Password in use"})

            user_object.password = password_change
            user_object.save()
            
            return Response("Done")
        except ValueError:
            raise ValidationError({ 'user_email': 'A valid input is required' , 'user_pass' : 'A valid input is required'})
        except ObjectDoesNotExist:
            raise ValidationError({ 'user not found': 'It appears your details are not registered'})


class UserLoginView(GenericAPIView):
    lookup_field = 'id'
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, format=None, id=None):
        try:
            user_email = request.data.get('user_email', None)
            user_phone = request.data.get('user_phone', None)
            password = request.data.get('user_pass', None)

            if (user_email is None and user_phone is None) or password is None:
                raise ValueError({ 'invalid input.' })

            user_object = None
            if user_phone is not None:
                user_object = User.objects.get(phone = user_phone)
            elif user_email is not None:
                user_object = User.objects.get(email = user_email)     
                
            if user_object is None:
                raise ValidationError({ 'User does not exist' })

            stored_password = user_object.password
            if stored_password != password:
                raise ValidationError({ 'Password does not match' })
            
            return Response(UserSerializer(user_object).data )
        except ValueError:
            raise ValidationError({ 'user_email': 'A valid input is required' , 'user_pass' : 'A valid input is required'})
        except ObjectDoesNotExist:
            raise ValidationError({ 'user not found': 'It appears your details are not registered'})


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
            user_phone = request.data.get('phone', None)
            user_email = request.data.get('email', None)
            name = request.data.get('name', None)
            phone = request.data.get('phone', None)
            company_id = request.data.get('company_id', None)
            company_name = request.data.get('company_name', None)
            session_duration = request.data.get('session_duration', None)
            password = request.data.get('password', None)

            queryset = User.objects.filter(phone = user_phone)
            queryset2 = User.objects.filter(email = user_email)
            # assert((str(user_phone)).startswith('+')) # User phone number must start with +
            
            if user_phone is None or user_email is None or name is None or phone is None or company_id is None or company_name is None or session_duration is None or password is None:
                raise ValidationError({"Error" : "Missing data. Must include data : 'name', 'phone', 'email', 'company_id', 'company_name', 'is_admin', 'password','session_duration'"})

            if user_phone is None or len(queryset.values_list()) > 0:
                raise ValidationError({ 'user phone number exists' })
            elif len(queryset2.values_list()) > 0:
                 raise ValidationError({ 'user email exists' })
        except ValueError:
            raise ValidationError({ 'user_phone': 'A valid number is required' })
        except AssertionError:
             raise ValidationError({ 'user_phone': 'Phone number must start with +' })
        # except :
        #     raise ValidationError({"Error": "An unknown error occured"})
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