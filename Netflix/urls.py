
from django.contrib import admin
from django.urls import path
from app1.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', HelloAPIView.as_view()),
    path('aktyorlar/', AktyorlarAPIView.as_view()),
    path('izohlar/', IzohlarAPIView.as_view()),
    path('bitta_aktyor/<int:pk>/', AktyorAPIView.as_view()),
    path('bitta_izoh/<int:pk>/', IzohAPIView.as_view()),
    path('aktyor_ochir/<int:pk>/', Aktyor_delAPIView.as_view()),
]
