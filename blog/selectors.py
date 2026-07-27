from django.shortcuts import get_object_or_404

from .models import Post


def get_post(pk):
    """A single post by primary key, or a 404 if it doesn't exist."""
    return get_object_or_404(Post, pk=pk)


def get_posts(author=None, date=None):
    """Posts newest-first, optionally narrowed to one author and/or the
    calendar date they were created on."""
    posts = Post.objects.all()
    if author:
        posts = posts.filter(author__username=author)
    if date:
        posts = posts.filter(created_at__date=date)
    return posts
