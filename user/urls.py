from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import *



urlpatterns = [
    path('user/', UserAPIView.as_view()), # http://127.0.0.1:8000/api/v1/user/
    path('user/<uuid:UUID>/', UserAPIView.as_view()), # http://127.0.0.1:8000/api/v1/user/
]