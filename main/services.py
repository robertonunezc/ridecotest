from django.contrib.auth.models import User


def get_owner_by_id(owner_id: int) -> User:
    return User.objects.get(pk=owner_id)
