from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("authors/", views.author_list, name="author_list"),
    path("by-author/", views.posts_by_author, name="posts_by_author"),
]
