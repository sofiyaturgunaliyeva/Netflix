
from django.contrib import admin
from django.urls import path,include
from app1.views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register("aktyorlar",AktyorModelViewset)
router.register("kinolar",KinoModelViewset)
router.register("izohlar",IzohModelViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', HelloAPIView.as_view()),
    path('', include(router.urls)),
    path('netf_token/',  obtain_auth_token),
    path('token_olish/',  TokenObtainPairView.as_view()),
    path('token_yangilash/',  TokenRefreshView.as_view()),
    path('aktyorlar_api/', AktyorlarAPIView.as_view()),
    path('izohlar_api/', IzohlarAPIView.as_view()),
    path('kinolar_api/', KinolarAPIView.as_view()),
    # path('bitta_aktyor/<int:pk>/', AktyorAPIView.as_view()),
    path('bitta_izoh/<int:pk>/', IzohAPIView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', Logout.as_view()),
    # path('bitta_kino/<int:pk>/', KinoAPIView.as_view()),
    # path('aktyor_ochir/<int:pk>/', Aktyor_delAPIView.as_view()),
    # path('kino/<int:pk>/', KinoDetailView.as_view()),
]
