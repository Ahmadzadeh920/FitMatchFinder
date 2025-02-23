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
#from ...RagClass import CutomizedRAG




class ProductListView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        api_key = self.kwargs.get('api_key')
        # Assuming List_API_Key has a field called 'key'
        api_key_instance = get_object_or_404(List_API_Key, key=api_key)
        return Product.objects.filter(API_KEY=api_key_instance)



class ProductDetailView(APIView):
    serializer_class = ProductSerializer
    def get_object(self, api_key, pk):
        try:
            # Assuming `List_API_Key` is the model that contains the API keys
            user = self.request.user
            api_key_instance = List_API_Key.objects.get(key=api_key , profile__user=user)
        
            return Product.objects.get(APIKey=api_key_instance, id=pk)
        except List_API_Key.DoesNotExist:
            raise NotFound("API Key not found.")
        except Product.DoesNotExist:
            raise NotFound("Product is not found.")

    def put(self, request, api_key, pk):
        Product_obj= self.get_object(api_key, pk)

        serializer = self.serializer_class(Product_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
                
                # 
            full_path = Product_obj.manual.path
                # desired_path includes API_Key/name image
            desired_path = "/".join(full_path.split("manual_collection")[-1:]).lstrip("/") 
            full_file_path = os.path.join(settings.MEDIA_ROOT,"manual_collection",desired_path)
                
            #colivara_obj = CutomizedRAG(collection= api_key)
            #syn_document = colivara_obj.sync_documents(full_file_path, pk)
            return Response(serializer.data)
    
