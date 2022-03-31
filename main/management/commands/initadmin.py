import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from grocery_list.models import GroceryList, GroceryCategory, Item


class Command(BaseCommand):

    def handle(self, *args, **options):
        # The magic line
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "user")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "user@local.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "1234567")
        print(username, password, email)
        owner = User.objects.create_superuser(username, email, password)
        grocery_category = GroceryCategory.objects.create(name="Category")
        GroceryList.objects.create(
            name="GL", owner=owner, category=grocery_category
        )

