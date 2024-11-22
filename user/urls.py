from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *



urlpatterns = [
#    path('user/', UserAPIView.as_view()), # http://127.0.0.1:8000/api/v1/user/
#    path('user/<int:pk>/', UserAPIView.as_view()), # http://127.0.0.1:8000/api/v1/user/pk/
    path('registration/', RegistrationAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('me/', CurrentUserView.as_view()),
    path('all/', ListUserAPIView.as_view()),
    path('<uuid:id>/', GetUserAPIView.as_view()),
    path('<uuid:id>/edit/', DeleteUpdateUserAPIView.as_view()),
    path('<uuid:id_user>/projects/', ListProjectsUser.as_view()),
    path('<uuid:id_user>/<uuid:id_project>/', ProjectUserAPIView.as_view()),
    path('<uuid:id_user>/<uuid:id_project>/<uuid:id_task>/', TaskProjectUserAPIView.as_view()),
    path('<uuid:id_user>/<uuid:id_project>/<uuid:id_task>/<uuid:id_comment>/', CommentTaskProjectUserAPIView.as_view()),
    # path('test/', serosadsad.as_view()),
]
