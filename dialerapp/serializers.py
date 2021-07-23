from rest_framework import serializers

from .models import User
from .models import Company

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'phone', 'email', 'company_id', 'company_name', 'is_admin', "session_duration", "password",)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'phone', 'playlist')
