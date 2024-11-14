from django.urls import path, include
from rest_framework import routers

from .views import *



urlpatterns = [
    path('project/', ProjectView.as_view()), # http://127.0.0.1:8000/api/v1/project/
    path('project/<int:pk>/', ProjectView.as_view())  # http://127.0.0.1:8000/api/v1/project/

]

# http://127.0.0.1:8000/api/v1/user/1
