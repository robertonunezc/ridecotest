from typing import List, Optional
from grocery_list.models import GroceryList, GroceryCategory, Item
from grocery_list import providers as grocery_list_providers
from main import services as main_services


def create_grocery_list(name: str, category_id: int, owner_id: int, is_private: bool = False) -> GroceryList:
    grocery_category = grocery_list_providers.get_category_by_id(category_id=category_id)
    owner = main_services.get_owner_by_id(owner_id=owner_id)
    grocery_list = GroceryList()
    grocery_list.name = name
    grocery_list.owner = owner
    grocery_list.category = grocery_category
    grocery_list.private = is_private
    grocery_list.save()
    return grocery_list


def add_item_to_grocery_list(grocery_list_id: int, name: str, note: Optional) -> Item:
    grocery_list = grocery_list_providers.get_grocery_list_by_id(grocery_list_id=grocery_list_id)
    grocery_list_item = Item()
    grocery_list_item.name = name
    grocery_list_item.note = note
    grocery_list_item.grocery_list = grocery_list
    grocery_list_item.save()
    return grocery_list_item


def get_all_grocery_lists() -> List["GroceryList"]:
    return grocery_list_providers.get_all_grocery_lists()
