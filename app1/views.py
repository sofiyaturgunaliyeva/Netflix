from django.contrib.auth import logout, authenticate
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status, filters
from rest_framework.viewsets import ModelViewSet
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework.authentication import TokenAuthentication

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

class AktyorlarAPIView(APIView):
    def get(self,requset):
        soz = requset.query_params.get('qidiruv')
        if soz:
            aktyorlar = Aktyor.objects.annotate(
                oxshashlik = TrigramSimilarity('ism',soz)
            ).filter(oxshashlik__gte = 0.1) # ism o'xshashligi 0.1 dan yuqori bo'lgan aktyorlar
        else:
            aktyorlar = Aktyor.objects.all()
        serializer = AktyorSerializer(aktyorlar,many=True)
        return Response(serializer.data)

    def post(self,request):
        malumot = request.data
        serializer = AktyorSerializer(data=malumot)
        if serializer.is_valid():
            Aktyor.objects.create(
                ism = serializer.validated_data.get('ism'),
                davlat = serializer.validated_data.get('davlat'),
                tugilgan_yili = serializer.validated_data.get('tugilgan_yili'),
                jins = serializer.validated_data.get('jins'),
            )
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


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



class KinolarAPIView(APIView):
    def get(self, request):
        soz = request.query_params.get('qidiruv')
        if soz:
            kinolar = Kino.objects.filter(nom__contains = soz)|Kino.objects.filter(
                janr = soz
            )
        else:
            kinolar = Kino.objects.all()
        serializer = KinoSerializer(kinolar, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self,request):
        kino = request.data
        serializer = KinoSaveSerializer(data = kino)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter] #  qidiruv uchun
    search_fields = ['ism','davlat'] # '__all__'    Ism va davlat orqali qidiradi
    ordering_fields = ['ism','tugilgan_yili','davlat']  # tartiblab chiqaradi


class KinoModelViewset(ModelViewSet):
    queryset = Kino.objects.all()
    serializer_class = KinoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # qidiruv uchun
    search_fields = ['nom', 'janr']  # '__all__'    Nom va janr orqali qidiradi
    ordering_fields = ['davomiylik', 'reyting']  # tartiblab chiqaradi

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

class LoginView(APIView):
    def post(self, request):
        malumot = request.data
        user = authenticate(username = malumot.get("username"),
                     password = malumot.get("password")
                     )
        if user is None:
            return Response({"success": "False", "xabar": "User topilmadi"})
        login(request, user)
        return Response({"success": "True", "xabar": "User login qilindi"})

class Logout(APIView):
    def get(self, request):
        logout(request)
        return Response({"success": "True", "xabar": "User logout qilindi"})

class IzohModelViewset(ModelViewSet):
    queryset = Izoh.objects.all()
    serializer_class = IzohSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Izoh.objects.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = IzohSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        izoh = self.get_object()
        if izoh.user != request.user:
            izoh.delete()
        return self.destroy(request, *args, **kwargs)
