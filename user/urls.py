from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *



urlpatterns = [

    path('registration/', RegistrationAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('me/', CurrentUserView.as_view()),
    path('<uuid:id>/', GetUserAPIView.as_view()),
    path('me/edit/', DeleteUpdateUserAPIView.as_view()),
    path('<uuid:id_user>/projects_roles/', ListProjectsUser.as_view()),
    path('<uuid:id_user>/<uuid:id_project>/', ProjectUserAPIView.as_view()),
    # path('<uuid:id_user>/<uuid:id_project>/<uuid:id_task>/', TaskProjectUserAPIView.as_view()),
    # path('<uuid:id_user>/<uuid:id_project>/<uuid:id_task>/<uuid:id_comment>/', CommentTaskProjectUserAPIView.as_view()),
]
