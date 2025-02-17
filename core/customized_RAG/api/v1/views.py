from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.conf import settings
import os
from celery.result import AsyncResult

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

from .serializers import ProductSerializer
from accounts.models import List_API_Key
from customized_RAG.models import Product
from django.shortcuts import get_object_or_404



class ProductListView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        api_key = self.kwargs.get('api_key')
        # Assuming List_API_Key has a field called 'key'
        api_key_instance = get_object_or_404(List_API_Key, key=api_key)
        return Product.objects.filter(API_KEY=api_key_instance)

    