from django.core.serializers import serialize
from rest_framework import serializers

from grocery_list.models import GroceryList, GroceryCategory, Item


class GroceryListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class GroceryListSerializer(serializers.ModelSerializer):
    items = GroceryListItemSerializer(many=True, required=False
                                      )
    class Meta:
        model = GroceryList
        fields = ['id', 'name', 'private', 'created', 'owner', 'category', 'items']
        depth = 1


class GroceryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GroceryCategory
        fields = '__all__'

