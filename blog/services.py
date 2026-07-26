from django.core.paginator import Paginator

POSTS_PER_PAGE = 5


def paginate(queryset, page_number):
    """Paginator.get_page() clamps out-of-range/non-numeric input to a
    valid page instead of raising, so callers never need to validate it."""
    return Paginator(queryset, POSTS_PER_PAGE).get_page(page_number)
