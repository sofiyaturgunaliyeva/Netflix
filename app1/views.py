from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import  status
from rest_framework.viewsets import ModelViewSet


class HelloAPIView(APIView):
    def get(self,request):
        d = {
            "xabar":"Salom dunyo !",
            "sana":"2023-06-22"
        }
        return Response(d)

    def post(self, request):
        malumot = request.data
        d = {
            "xabar": "Post qabul qilindi",
            "post_malumoti": malumot
        }
        return Response(d)

# class AktyorlarAPIView(APIView):
#     def get(self,requset):
#         aktyorlar = Aktyor.objects.all()
#         serializer = AktyorSerializer(aktyorlar,many=True)
#         return Response(serializer.data)
#
#     def post(self,request):
#         malumot = request.data
#         serializer = AktyorSerializer(data=malumot)
#         if serializer.is_valid():
#             Aktyor.objects.create(
#                 ism = serializer.validated_data.get('ism'),
#                 davlat = serializer.validated_data.get('davlat'),
#                 tugilgan_yili = serializer.validated_data.get('tugilgan_yili'),
#                 jins = serializer.validated_data.get('jins'),
#             )
#             return Response(serializer.data,status = status.HTTP_201_CREATED)
#         return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


# class AktyorAPIView(APIView):
#     def get(self,request,pk):
#         aktyor = Aktyor.objects.get(id = pk)
#         serializer = AktyorSerializer(aktyor)
#         return Response(serializer.data)


# Vazifa
# 1. Izoh jadvali uchun serializer va hamma izohlarni chiqaruvchi APIView yozing.
# 2. Yangi izoh qo’shish uchun APIView yozing.


class IzohlarAPIView(APIView):
    def get(self, request):
        izohlar = Izoh.objects.all()
        serializer = IzohSerializer(izohlar, many=True)
        return Response(serializer.data)


    def post(self,request):
        malumot = request.data
        serializer = IzohSerializer(data=malumot)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# 3. Tanlangan bitta izohni ko'rish uchun APIView yozing.

class IzohAPIView(APIView):
    def get(self,request,pk):
        izoh = Izoh.objects.get(id = pk)
        serializer = IzohSerializer(izoh)
        return Response(serializer.data)


#     4. Tanlangan bitta aktyorni o’chirish uchun APIView yozing.

# class Aktyor_delAPIView(APIView):
#     def delete(self,request,pk):
#         aktyor = Aktyor.objects.get(id=pk)
#         aktyor.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# class KinolarAPIView(APIView):
#     def get(self, request):
#         kinolar = Kino.objects.all()
#         serializer = KinoSerializer(kinolar, many=True)
#         return Response(serializer.data, status = status.HTTP_200_OK)

    # def post(self,request):
    #     kino = request.data
    #     serializer = KinoSaveSerializer(data = kino)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class KinoDetailView(APIView):
#     def put(self,request,pk):
#         kino = Kino.objects.get(id = pk)
#         malumot = request.data
#         serializer = KinoSaveSerializer(kino, data=malumot)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class KinoAPIView(APIView):
#     def get(self,request,pk):
#         kino = Kino.objects.get(id = pk)
#         serializer = KinoSerializer(kino)
#         return Response(serializer.data)
#     def delete(self,request,pk):
#         Kino.objects.filter(id = pk).delete()
#         return Response({"xabar":"Kino ma'lumoti o'chirildi1"},status=status.HTTP_204_NO_CONTENT)



class AktyorModelViewset(ModelViewSet):
    queryset = Aktyor.objects.all()
    serializer_class = AktyorSerializer


class KinoModelViewset(ModelViewSet):
    queryset = Kino.objects.all()
    serializer_class = KinoSerializer

    @action(detail=True,methods=['GET','POST'])
    def aktyorlar(self,request,pk): # kinolar/1/aktyorlar
        if request.method == 'POST':
            aktyor = request.data
            kino = self.get_object()
            serializer = AktyorSerializer(data = aktyor)
            if serializer.is_valid():
                a = Aktyor.objects.create(
                    ism=serializer.validated_data.get('ism'),
                    davlat = serializer.validated_data.get('davlat'),
                    tugilgan_yili = serializer.validated_data.get('tugilgan_yili'),
                    jins = serializer.validated_data.get('jins')

                )
                kino.aktyorlar.add(a)
                kino.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)
        kino = self.get_object() # == Kino.objects.get(id = pk)
        actors = kino.aktyorlar.all()
        serializer = AktyorSerializer(actors,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
