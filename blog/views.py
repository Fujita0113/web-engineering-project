from django.http import HttpResponse

from accounts.models import User

from .models import Post


def post_list(request):
    """All posts, newest first (Post.Meta orders by -created_at)."""
    posts = Post.objects.all()
    lines = [f"{p.created_at:%Y-%m-%d} | {p.title} | {p.author}" for p in posts]
    body = "All posts (newest first):\n\n" + "\n".join(lines)
    return HttpResponse(body, content_type="text/plain; charset=utf-8")


def author_list(request):
    """List of all authors."""
    authors = User.objects.all()
    body = "Authors:\n\n" + "\n".join(str(a) for a in authors)
    return HttpResponse(body, content_type="text/plain; charset=utf-8")


def posts_by_author(request):
    """Posts by a single author.

    Exercise 6: the author name is hard-coded for now; it will become a
    URL argument in a later exercise.
    """
    author_name = "alice"
    posts = Post.objects.filter(author__username=author_name)
    lines = [f"{p.created_at:%Y-%m-%d} | {p.title}" for p in posts]
    body = f"Posts by {author_name}:\n\n" + "\n".join(lines)
    return HttpResponse(body, content_type="text/plain; charset=utf-8")
