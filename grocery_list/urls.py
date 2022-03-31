
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from grocery_list import views
app_name = 'grocery_list'
urlpatterns = [
    path('', views.GroceryListView.as_view(), name="grocery_lists"),
    path('<int:pk>', views.GroceryListDetailsView.as_view(), name="grocery_list_details"),
    path('item', views.GroceryListItemView.as_view(), name="grocery_list_add_item"),
    path('item/<int:pk>', views.GroceryListItemView.as_view(), name="grocery_list_items"),
    path('categories', views.GroceryCategoryListView.as_view(), name="category_lists"),

]

urlpatterns = format_suffix_patterns(urlpatterns)