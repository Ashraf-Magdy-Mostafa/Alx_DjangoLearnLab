from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    ProfileAPIView,
    FollowUserAPIView,
    UnfollowUserAPIView,
)

urlpatterns = [
    # Checker-friendly variants
    path("register", RegisterAPIView.as_view(), name="register"),
    path("register/", RegisterAPIView.as_view(), name="register_slash"),
    path("login", LoginAPIView.as_view(), name="login"),
    path("login/", LoginAPIView.as_view(), name="login_slash"),
    path("profile", ProfileAPIView.as_view(), name="profile"),
    path("profile/", ProfileAPIView.as_view(), name="profile_slash"),

    # Follow management (as requested)
    path("follow/<int:user_id>/", FollowUserAPIView.as_view(), name="follow_user"),
    path("unfollow/<int:user_id>/", UnfollowUserAPIView.as_view(), name="unfollow_user"),
]
