
from django.contrib import admin
from django.urls import path,include
from app1.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("aktyorlar",AktyorModelViewset)
router.register("kinolar",KinoModelViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', HelloAPIView.as_view()),
    path('', include(router.urls)),
    # path('aktyorlar/', AktyorlarAPIView.as_view()),
    path('izohlar/', IzohlarAPIView.as_view()),
    # path('kinolar/', KinolarAPIView.as_view()),
    # path('bitta_aktyor/<int:pk>/', AktyorAPIView.as_view()),
    path('bitta_izoh/<int:pk>/', IzohAPIView.as_view()),
    # path('bitta_kino/<int:pk>/', KinoAPIView.as_view()),
    # path('aktyor_ochir/<int:pk>/', Aktyor_delAPIView.as_view()),
    # path('kino/<int:pk>/', KinoDetailView.as_view()),
]
