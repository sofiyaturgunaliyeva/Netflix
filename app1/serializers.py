from rest_framework import serializers
from .models import *

class AktyorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    ism = serializers.CharField(max_length=50)
    davlat = serializers.CharField(max_length=50)
    tugilgan_yili = serializers.CharField(max_length=50)
    jins = serializers.CharField(max_length=50)


class IzohSerializer(serializers.ModelSerializer):
    class Meta:
        model = Izoh
        fields = '__all__'