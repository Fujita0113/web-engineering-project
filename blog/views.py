from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_date

from accounts.models import User

from .forms import PostForm
from .models import Post
from .selectors import get_post, get_posts
from .services import paginate


def _querystring_without_page(request):
    """Current GET params minus `page`, for building Previous/Next links."""
    params = request.GET.copy()
    params.pop("page", None)
    return params.urlencode()


def post_list(request):
    """All posts, newest first, optionally narrowed to one calendar date."""
    date_str = request.GET.get("date", "").strip()
    date = parse_date(date_str) if date_str else None
    posts = paginate(get_posts(date=date), request.GET.get("page"))
    context = {"posts": posts, "date": date_str, "querystring": _querystring_without_page(request)}
    return render(request, "blog/post_list.html", context)


def post_detail(request, pk):
    """The full content of a single post."""
    post = get_post(pk)
    return render(request, "blog/post_detail.html", {"post": post})


def author_list(request):
    """List of all authors."""
    authors = User.objects.all()
    return render(request, "blog/author_list.html", {"authors": authors})


def posts_by_author(request):
    """Posts by a single author, chosen via the `?author=` GET parameter and
    optionally narrowed further by the `?date=` GET parameter.

    Replaces the Exercise 6 stub (hard-coded author): the author name now comes
    from user input. With no author given, only the search form is shown.
    """
    author = request.GET.get("author", "").strip()
    date_str = request.GET.get("date", "").strip()
    date = parse_date(date_str) if date_str else None
    posts = paginate(get_posts(author=author, date=date), request.GET.get("page")) if author else Post.objects.none()
    context = {
        "author": author,
        "date": date_str,
        "posts": posts,
        "querystring": _querystring_without_page(request),
    }
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
