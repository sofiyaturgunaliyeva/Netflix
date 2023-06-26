from rest_framework import serializers
from .models import *
from rest_framework.exceptions import APIException

class AktyorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    ism = serializers.CharField(max_length=50)
    davlat = serializers.CharField(max_length=50)
    tugilgan_yili = serializers.CharField(max_length=50)
    jins = serializers.CharField(max_length=50)

    def validate_ism(self,qiymat):
        if len(qiymat) < 3:
            raise serializers.ValidationError("Ism bunday kalta bo'lishi mumkin emas")
        return qiymat


class IzohSerializer(serializers.ModelSerializer):
    class Meta:
        model = Izoh
        fields = '__all__'

    def validate_baho(self,baho):
        if baho <= 1 <= 5:
            return baho
        raise serializers.ValidationError("Bunday baho yo'q")
    def validate_matn(self, matn):
        if "Yomon" in matn or "O'rtacha" in matn or "O'xshamapti" in matn:
            raise serializers.ValidationError("Bunday izoh ozish mumkin emas")
        return matn


class KinoSerializer(serializers.ModelSerializer):
    aktyorlar = AktyorSerializer(many = True)
    class Meta:
        model = Kino
        fields = '__all__'

class KinoSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kino
        fields = '__all__'