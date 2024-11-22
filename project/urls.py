from django.urls import path, include
from rest_framework import routers

from .views import *



urlpatterns = [
    # path('project/', ProjectView.as_view()), # http://127.0.0.1:8000/api/v1/project/
    # path('project/<int:pk>/', ProjectView.as_view()),  # http://127.0.0.1:8000/api/v1/project/
    # path('project/<int:pk>/roles/', RolesView.as_view()),  # http://127.0.0.1:8000/api/v1/project/
    path('all/', ProjectAll.as_view()),
    path('<uuid:id>/', ProjectByUUID.as_view()),
    path('<uuid:id>/edit/', ProjectEdit.as_view()),

]

'''
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
'''