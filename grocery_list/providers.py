from grocery_list.models import GroceryCategory, GroceryList


def get_category_by_id(category_id:int) -> GroceryCategory:
    return GroceryCategory.objects.get(pk=category_id)


def get_grocery_list_by_id(grocery_list_id: int) -> GroceryList:
    return GroceryList.objects.get(pk=grocery_list_id)


def get_all_grocery_lists() -> "QuerySet[GroceryList]":
    return GroceryList.objects.all()
