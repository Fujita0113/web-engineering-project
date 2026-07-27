from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("posts/<int:pk>/", views.post_detail, name="post_detail"),
    path("authors/", views.author_list, name="author_list"),
    path("by-author/", views.posts_by_author, name="posts_by_author"),
    path("new/", views.post_create, name="post_create"),
]
