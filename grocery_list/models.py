from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class GroceryCategory(models.Model):
    name = models.CharField(max_length=150)
    class Meta:
        verbose_name = "GroceryCategory"
        verbose_name_plural = "GroceryCategories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("GroceryCategory_detail", kwargs={"pk": self.pk})


class GroceryList(models.Model):
    name = models.CharField(max_length=150)
    private = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="grocery_lists")
    category = models.ForeignKey(GroceryCategory, on_delete=models.PROTECT,  related_name="grocery_lists")
    class Meta:
        verbose_name = "GroceryList"
        verbose_name_plural = "GroceryLists"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("GroceryList_detail", kwargs={"pk": self.pk})


class Item(models.Model):
    name = models.CharField(max_length=150)
    note = models.TextField(null=True, blank=True)
    purchased = models.BooleanField(default=False)
    grocery_list = models.ForeignKey(GroceryList, on_delete=models.PROTECT, related_name="items")

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ["purchased"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Item_detail", kwargs={"pk": self.pk})

