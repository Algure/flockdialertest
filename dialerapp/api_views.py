from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView,RetrieveUpdateDestroyAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from dialerapp.models import User
from dialerapp.models import Company
from dialerapp.serializers import UserSerializer
from dialerapp.serializers import CompanySerializer


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
            phone = request.data.get('phone')
            queryset = User.objects.filter(name='Helen')
            if price is not None and float(price) <= 0.0:
                raise ValidationError({ 'price': 'Must be above $0.00' })
        except ValueError:
            raise ValidationError({ 'price': 'A valid number is required' })
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
