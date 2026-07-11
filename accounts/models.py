from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Blog author.

    Extends Django's built-in user, so it already has ``username`` (unique),
    ``password`` and ``date_joined`` (used as the creation timestamp).
    Kept as a custom model from the start so it can be extended later
    without a painful migration.
    """

    def __str__(self):
        return self.username
