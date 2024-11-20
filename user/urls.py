from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *



urlpatterns = [
    path('user/', UserAPIView.as_view()), # http://127.0.0.1:8000/api/v1/user/
    path('user/<int:pk>/', UserAPIView.as_view()), # http://127.0.0.1:8000/api/v1/user/pk/

    path('user/registration/', RegistrationAPIView.as_view()),

    path('user/token/', TokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
    # path("user/auth/", include("rest_framework.urls")),

    path('user/halo/', my_protected_function)
]