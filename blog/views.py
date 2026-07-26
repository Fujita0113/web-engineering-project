from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import User

from .forms import PostForm
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
    context = {"author": author, "posts": posts}
    # HTMX requests get only the results fragment; browsers get the full page.
    if request.headers.get("HX-Request"):
        return render(request, "blog/_post_results.html", context)
    return render(request, "blog/posts_by_author.html", context)


@login_required
def post_create(request):
    """Create a post as the logged-in user. Anonymous requests are redirected
    to the login page by @login_required (both GET and POST)."""
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:post_list")
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form})
