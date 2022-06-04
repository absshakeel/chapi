
from django.urls import path
from .views import *

urlpatterns = [
    path("profile/",ProfileView.as_view(),name="profile"),
    path("register/",RegisterView.as_view(),name="register"),
    path("updateuser/",UserDataUpdate.as_view(),name="updateuser"),
    path("updateprofile/",Updateprofile.as_view(),name="updateprofile"),
]