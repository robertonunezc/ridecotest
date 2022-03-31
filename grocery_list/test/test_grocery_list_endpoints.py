from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from grocery_list.models import GroceryList, GroceryCategory, Item

GROCERY_LIST_DETAILS_URL = 'grocery_list:grocery_list_details'


class TestGroceryList(TestCase):
    @classmethod
    def setUp(self):
        self.grocery_category = GroceryCategory.objects.create(name="Category")

        self.user = User.objects.create_user(
            username='test', email='test@rideco.com', password='Us3r123.')
        self.token = self.user.auth_token
        self.client_drf = APIClient()
        self.client_drf.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)

        self.grocery_list = GroceryList.objects.create(
            name="GL", owner=self.user, category=self.grocery_category
        )

    def test_add_item_to_grocery_list(self):
        data = {
            'grocery_list': self.grocery_list.pk,
            'name': "ITEM",
            'note': "MY NOTE"
        }
        response = self.client_drf.post(reverse('grocery_list:grocery_list_add_item'), data=data, format='json')
        items = Item.objects.all()
        self.assertEqual(len(items), 1)
        self.assertEqual(response.status_code, 201)

    def test_create_grocery_list(self):
        data = {
            'name': "GLNAME",
            'category_id': self.grocery_category.pk,
            'is_private': 0,
            'owner_id': self.user.pk
        }
        response = self.client_drf.post(reverse('grocery_list:grocery_lists'), data=data, format='json')
        grocery_lists = GroceryList.objects.all()
        self.assertEqual(len(grocery_lists), 2)
        self.assertEqual(response.status_code, 201)

    def test_get_all_grocery_list(self):
        response = self.client_drf.get(reverse('grocery_list:grocery_lists'))
        grocery_lists = GroceryList.objects.all()
        self.assertEqual(len(grocery_lists), 1)
        self.assertEqual(response.status_code, 200)

    def test_get_grocery_list_details_by_id(self):
        response = self.client_drf.get(reverse('grocery_list:grocery_list_details', kwargs={'pk': self.grocery_list.pk}))
        self.assertEqual(response.data['name'], self.grocery_list.name)
        self.assertEqual(response.status_code, 200)

    def test_delete_grocery_list_by_id(self):
        response = self.client_drf.delete(reverse(GROCERY_LIST_DETAILS_URL, kwargs={'pk': self.grocery_list.pk}))
        grocery_lists = GroceryList.objects.all()
        self.assertEqual(len(grocery_lists), 0)
        self.assertEqual(response.status_code, 204)

    def test_update_grocery_list(self):
        initial_grocery_data = self.grocery_list
        data = {
            'name': "GLNAME",

        }
        response = self.client_drf.patch(reverse(GROCERY_LIST_DETAILS_URL, kwargs={'pk': self.grocery_list.pk}), data=data, format='json')
        grocery_list = GroceryList.objects.all().order_by('-id').first()
        self.assertNotEqual(grocery_list.name, initial_grocery_data.name)
        self.assertEqual(response.status_code, 200)