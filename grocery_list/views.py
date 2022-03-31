from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from grocery_list.exceptions import GroceryListException, GroceryListItemException
from ridecotest.permissions import BearerTokenAuth
from grocery_list.models import GroceryList, GroceryCategory, Item
from grocery_list.serializers import GroceryListSerializer, GroceryCategorySerializer, GroceryListItemSerializer
from grocery_list import services as grocery_list_services
from grocery_list import providers as grocery_list_providers


# Create your views here.
class GroceryListItemView(generics.CreateAPIView):
    serializer = GroceryListItemSerializer
    authentication_classes = [BearerTokenAuth]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except GroceryListItemException.DoesNotExist:
            raise Http404

    def create(self, request, *args, **kwargs):
        try:
            grocery_list_services.add_item_to_grocery_list(grocery_list_id=request.data['grocery_list'],
                                                           name=request.data['name'],
                                                           note=request.data.get('note', None),
                                                           )

        except GroceryListItemException:
            return Response("GroceryListItemException", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        item = self.get_object(pk=pk)
        serializer = GroceryListItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk=pk)
        item.delete()
        return Response({"Deleted item"},status=status.HTTP_204_NO_CONTENT)


class GroceryListView(generics.ListCreateAPIView):
    queryset = grocery_list_providers.get_all_grocery_lists()
    serializer_class = GroceryListSerializer
    authentication_classes = [BearerTokenAuth]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            grocery_list = grocery_list_services.create_grocery_list(name=request.data['name'],
                                                      category_id=request.data['category_id'],
                                                      is_private=request.data['is_private'],
                                                      owner_id=request.data['owner_id']
                                                      )
            serializer = GroceryListSerializer(grocery_list)

        except GroceryListException:
            return Response("GroceryListException", status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroceryListDetailsView(APIView):
    serializer_class = GroceryListSerializer
    authentication_classes = [BearerTokenAuth]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return GroceryList.objects.get(pk=pk)
        except GroceryList.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        grocery_list = self.get_object(pk)
        serializer = GroceryListSerializer(instance=grocery_list)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        grocery_list = self.get_object(pk)
        serializer = GroceryListSerializer(grocery_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        grocery_list = self.get_object(pk)
        grocery_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroceryCategoryListView(generics.ListAPIView):
    queryset = GroceryCategory.objects.all()
    serializer_class = GroceryCategorySerializer
    authentication_classes = [BearerTokenAuth]
    permission_classes = [IsAuthenticated]
