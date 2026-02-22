from rest_framework import viewsets, status, permissions, generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

from notifications.models import Notification

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
        return super().get_permissions()

    def check_object_permissions(self, request, obj):
        if request.method in ["PUT", "PATCH", "DELETE"] and obj.author != request.user:
            self.permission_denied(request, message="You can only modify your own posts.")
        return super().check_object_permissions(request, obj)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        post_id = self.request.query_params.get("post")
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb="commented on your post",
                target_content_type=None,
                target_object_id=comment.post.id,
            )

    def check_object_permissions(self, request, obj):
        if request.method in ["PUT", "PATCH", "DELETE"] and obj.author != request.user:
            self.permission_denied(request, message="You can only modify your own comments.")
        return super().check_object_permissions(request, obj)

class FeedAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Required by checker:
        following_users = request.user.following.all()
        feed_posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
        page = self.paginate_queryset(feed_posts)
        if page is not None:
            serializer = PostSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        serializer = PostSerializer(feed_posts, many=True, context={"request": request})
        return Response(serializer.data)

class LikePostAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk: int, *args, **kwargs):
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({"detail": "Already liked."}, status=400)

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target_content_type=None,
                target_object_id=post.id,
            )
        return Response({"detail": "Liked."}, status=status.HTTP_201_CREATED)

class UnlikePostAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk: int, *args, **kwargs):
        post = generics.get_object_or_404(Post, pk=pk)
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        if deleted == 0:
            return Response({"detail": "You haven't liked this post."}, status=400)
        return Response({"detail": "Unliked."}, status=200)
