from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth.models import User
from grocery_list import services as grocery_list_services
from grocery_list.models import GroceryCategory, GroceryList, Item


class TestGroceryList(TestCase):
    @classmethod
    def setUp(self):
        self.grocery_category = GroceryCategory.objects.create(name="Category")
        self.owner = User.objects.create_user(
            username='test', email='test@rideco.com', password='Us3r123.')
        self.grocery_list = GroceryList.objects.create(
            name="GL", owner=self.owner, category=self.grocery_category
        )

    def test_create_grocery_list(self):
        grocery_list_services.create_grocery_list(name="GRLIST", category_id=self.grocery_category.pk, owner_id=self.owner.pk, is_private=True)
        grocery_lists = GroceryList.objects.all()
        # The assert is with 2 because in the setUp we create another GroceryList
        self.assertEqual(len(grocery_lists), 2)

    @patch("grocery_list.services.grocery_list_providers.get_grocery_list_by_id")
    def test_add_item_to_grocery_list(self, mock_get_grocery_list_by_id):
        mock_get_grocery_list_by_id.return_value = self.grocery_list
        grocery_list_services.add_item_to_grocery_list(grocery_list_id=1, name="ITEM", note="NTAA")
        items = Item.objects.all()
        self.assertEqual(len(items), 1)

