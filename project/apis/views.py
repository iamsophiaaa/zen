from django.shortcuts import render
from rest_framework import viewsets
from core.models import MenuItem
from .serializers import MenuItemModelSerializer
# Create your views here.
class MenuItemModelViewset(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemModelSerializer