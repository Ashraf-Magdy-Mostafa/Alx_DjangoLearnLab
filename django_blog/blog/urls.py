from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Auth
    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="blog/logout.html"), name="logout"),
    path("profile/", views.profile_view, name="profile"),

    # Posts
    path("", views.PostListView.as_view(), name="post_list"),
    path("posts/new/", views.PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
    path("posts/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),

    # Comments
    path("posts/<int:post_id>/comments/new/", views.CommentCreateView.as_view(), name="comment_create"),
    path("comments/<int:pk>/edit/", views.CommentUpdateView.as_view(), name="comment_edit"),
    path("comments/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment_delete"),

    # Search + Tags
    path("search/", views.SearchView.as_view(), name="search"),
    path("tags/<str:tag_name>/", views.TagPostsView.as_view(), name="tag_posts"),
]
