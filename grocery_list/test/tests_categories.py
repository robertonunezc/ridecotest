from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from grocery_list.models import GroceryCategory


class TestGroceryCategories(TestCase):
    @classmethod
    def setUp(self):
        self.categories = [GroceryCategory("category"), GroceryCategory("category_2")]
        self.user = User.objects.create_user(
            username='test', email='test@rideco.com', password='Us3r123.')
        self.token = self.user.auth_token
        self.client_drf = APIClient()
        self.client_drf.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)

    def test_get_all_categories(self):
        response = self.client_drf.get(reverse('grocery_list:category_lists'))
        self.assertEqual(response.status_code, 200)
