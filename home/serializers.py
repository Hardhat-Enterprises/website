from rest_framework import serializers
from .models import APIModel
class APIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIModel
        fields = '__all__'