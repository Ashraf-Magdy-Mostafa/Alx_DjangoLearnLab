from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

from notifications.utils import create_notification

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author").all().order_by("-created_at")
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy", "like", "unlike", "feed"]:
            return [IsAuthenticated()]
        return []

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def get_object_permissions(self):
        return [IsOwnerOrReadOnly()]

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def check_object_permissions(self, request, obj):
        # owner only for modifications
        if request.method in ["PUT", "PATCH", "DELETE"]:
            perm = IsOwnerOrReadOnly()
            if not perm.has_object_permission(request, self, obj):
                self.permission_denied(request, message="You can only modify your own posts.")
        return super().check_object_permissions(request, obj)

    @action(detail=False, methods=["get"], url_path="feed", permission_classes=[IsAuthenticated])
    def feed(self, request):
        following_ids = request.user.following.values_list("id", flat=True)
        qs = Post.objects.filter(author_id__in=following_ids).select_related("author").order_by("-created_at")
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="like", permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({"detail": "Already liked."}, status=400)
        # notify post owner (if not self)
        if post.author != request.user:
            create_notification(recipient=post.author, actor=request.user, verb="liked your post", target=post)
        return Response({"detail": "Liked."}, status=201)

    @action(detail=True, methods=["post"], url_path="unlike", permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        deleted, _ = Like.objects.filter(post=post, user=request.user).delete()
        if deleted == 0:
            return Response({"detail": "You haven't liked this post."}, status=400)
        return Response({"detail": "Unliked."}, status=200)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author", "post").all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        post_id = self.request.query_params.get("post")
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # notify post owner (if not self)
        if comment.post.author != self.request.user:
            create_notification(recipient=comment.post.author, actor=self.request.user, verb="commented on your post", target=comment.post)

    def check_object_permissions(self, request, obj):
        # owner only for modifications
        if request.method in ["PUT", "PATCH", "DELETE"]:
            if obj.author != request.user:
                self.permission_denied(request, message="You can only modify your own comments.")
        return super().check_object_permissions(request, obj)
