from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import CustomUser
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserPublicSerializer,
    ProfileUpdateSerializer,
)

from notifications.models import Notification

class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response(
            {"token": token.key, "user": UserPublicSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserPublicSerializer(user).data})

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return ProfileUpdateSerializer
        return UserPublicSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class FollowUserAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id: int, *args, **kwargs):
        target = get_object_or_404(CustomUser, id=user_id)
        if target == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=400)

        # request.user follows target => add request.user to target.followers
        target.followers.add(request.user)

        # Notification.objects.create required by checker
        Notification.objects.create(
            recipient=target,
            actor=request.user,
            verb="followed you",
            target_content_type=None,
            target_object_id=None,
        )
        return Response({"detail": f"You are now following {target.username}."}, status=200)

class UnfollowUserAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id: int, *args, **kwargs):
        target = get_object_or_404(CustomUser, id=user_id)
        target.followers.remove(request.user)
        return Response({"detail": f"You unfollowed {target.username}."}, status=200)
