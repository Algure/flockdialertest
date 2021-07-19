from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView,RetrieveUpdateDestroyAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from dialerapp.models import User
from dialerapp.models import Company
from dialerapp.serializers import UserSerializer

class DataPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id', 'company_id')
    search_fields = ('name', 'company_name')
    pagination_class = DataPagination

class UserCreate(CreateAPIView):
    serializer_class = UserSerializer

    # def create(self, request, *args, **kwargs):
    #     try:
    #         price = request.data.get('price')
    #         if price is not None and float(price) <= 0.0:
    #             raise ValidationError({ 'price': 'Must be above $0.00' })
    #     except ValueError:
    #         raise ValidationError({ 'price': 'A valid number is required' })
    #     response = super().create(request, *args, **kwargs)

class UserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializer

