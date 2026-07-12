from django.shortcuts import render

from accounts.models import User

from .models import Post


def post_list(request):
    """All posts, newest first (Post.Meta orders by -created_at)."""
    posts = Post.objects.all()
    return render(request, "blog/post_list.html", {"posts": posts})


def author_list(request):
    """List of all authors."""
    authors = User.objects.all()
    return render(request, "blog/author_list.html", {"authors": authors})


def posts_by_author(request):
    """Posts by a single author, chosen via the `?author=` GET parameter.

    Replaces the Exercise 6 stub (hard-coded author): the author name now comes
    from user input. With no author given, only the search form is shown.
    """
    author = request.GET.get("author", "").strip()
    posts = Post.objects.filter(author__username=author) if author else Post.objects.none()
    return render(request, "blog/posts_by_author.html", {"author": author, "posts": posts})
