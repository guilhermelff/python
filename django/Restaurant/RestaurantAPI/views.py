
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from.models import MenuItem, Category
from.serializers import MenuItemSerializer, CategorySerializer



# Create your views here.

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = (MenuItem.objects.all())
    serializer_class = MenuItemSerializer

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SingleCategoryView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = (Category.objects.all())
    serializer_class = CategorySerializer