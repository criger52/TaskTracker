from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'project', UserViewSet) # хуйни тут корочи вьюсет который тебе адао прописать в вьюхе

urlpatterns = [
    path('', include(router.urls)) # http://127.0.0.1:8000/api/v1/user/
    #path('user/', UserAPIList.as_view()),
    #path('user/<int:pk>/', UserAPIUpdate.as_view()),
    #path('userdelete/<int:pk>/', UserAPIDestroy.as_view())

]

# http://127.0.0.1:8000/api/v1/user/1
