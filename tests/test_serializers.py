from django.test import TestCase

from app1.models import *
from app1.serializers import *
from rest_framework.authtoken.admin import User


class TestAktyorSerializer(TestCase):
    def setUp(self) -> None:
        pass

    def test_aktyorlar(self):
        aktyorlar = Aktyor.objects.all()
        serializer = AktyorSerializer(aktyorlar, many = True)
        assert len(aktyorlar) == len(serializer.data)


    def test_valid_aktyor(self):
        d = {"id":1, "ism": "Vincent", "jins": "Erkak",
             "tugilgan_yili":"1991-03-23","davlat":"Belgiya"}
        serializer = AktyorSerializer(data=d)
        assert serializer.is_valid() == True
        assert serializer.validated_data.get("ism") == "Vincent"
        assert serializer.validated_data.get("jins") == "Erkak"
        assert serializer.validated_data.get("davlat") == "Belgiya"
        # assert serializer.validated_data.get("id") is not None

    def test_invalid_aktyor(self):
        d = {"id": 2, "ism": "Ab", "jins": "Erkak",
             "tugilgan_yili": "1991-03-23", "davlat": "Belgiya"}
        serializer = AktyorSerializer(data=d)
        assert serializer.is_valid() == False
        assert serializer.errors.get("ism")[0] == "Ism bunday kalta bo'lishi mumkin emas"



class TestIzohSerializer(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(username="user", password="1")
        self.kino1 = Kino.objects.create(nom="Titanik", janr="Action", reyting=8.5)
        self.aktyor = Aktyor.objects.create(ism="Ali", jins="Erkak",
                                       tugilgan_yili="1991-03-23", davlat="Belgiya")
        self.kino1.aktyorlar.add(self.aktyor)
        self.kino1.save()

    def test_valid_izoh(self):
        d = {"id":1, "matn": "Yaxshi", "baho": 3, "user": self.user1.id, "kino": self.kino1.id, "sana": "2023-07-15"}
        serializer = IzohSerializer(data=d)
        assert serializer.is_valid() == True
        assert True == True

    def test_invalid_izoh(self):
        d2 = {"id": 2, "matn": "Yaxshi", "baho": 12, "user": self.user1.id, "kino": self.kino1.id, "sana": "2023-07-15"}
        serializer = IzohSerializer(data=d2)
        assert serializer.is_valid() == False
        # assert serializer.validated_data.get("davlat") == "Belgiya"