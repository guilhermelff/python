
from rest_framework import generics
from.models import MenuItem
from.serializers import MenuItemSerializer


# Create your views here.

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = (MenuItem.objects.all())
    serializer_class = MenuItemSerializer