from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.conf import settings
import os
from celery.result import AsyncResult
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from customized_RAG.api.v1.serializers import ProductSerializer, QuerySerializer, ProductUpdateSerializer
from accounts.models import List_API_Key
from customized_RAG.models import Product,Query
from django.shortcuts import get_object_or_404
from customized_RAG.tasks import process_doc_rag, delete_doc_rag
from customized_RAG.ColivaraRAG import ColivaraRAG
from django.core.files.base import ContentFile
import io
from PIL import Image as PILImage
import base64






class ProductListView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        api_key = self.kwargs.get('api_key')
        # Assuming List_API_Key has a field called 'key'
        api_key_instance = get_object_or_404(List_API_Key, key=api_key)
        return Product.objects.filter(APIKey=api_key_instance)
    
    def perform_create(self, serializer):
        api_key = self.kwargs.get('api_key')
        api_key_instance = get_object_or_404(List_API_Key, key=api_key)
        serializer.save(APIKey=api_key_instance)



class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.request and self.request.method in ['PUT', 'PATCH']:
            return ProductUpdateSerializer  # Use the update serializer for PATCH/PUT
        return super().get_serializer_class()  # Default for GET/DELETE
    def get_object(self):
        api_key = self.kwargs.get('api_key')
        pk = self.kwargs.get('pk')
        # Assuming List_API_Key has a field called 'key'
        # and Product has a ForeignKey to List_API_Key
        try:
            # Assuming `List_API_Key` is the model that contains the API keys
            user = self.request.user
            api_key_instance = List_API_Key.objects.get(key=api_key , profile__user=user)
        
            return Product.objects.get(APIKey=api_key_instance, id=pk)
        except List_API_Key.DoesNotExist:
            raise NotFound("API Key not found.")
        except Product.DoesNotExist:
            raise NotFound("Product is not found.")
        
    
    def perform_update(self, serializer):
        Product_obj= self.get_object()
 
        updated_product = serializer.save()
        full_file_path =updated_product.manual_file.path
        # desired_path includes API_Key/name image
        '''
        desired_path = "/".join(full_path.split("manual_collection")[-1:]).lstrip("/") 
        full_file_path = os.path.join(settings.MEDIA_ROOT,"manual_collection",desired_path)
        '''
        pk= updated_product.id
        api_key= updated_product.APIKey.key
        if updated_product.Processing_boolean ==True and Product_obj.Processing_boolean== False:
            # 
        
            process_doc_rag.apply_async(args= [api_key, full_file_path, pk])  # Call the Celery task
                
            return Response(serializer.data)
        
        
    def perform_destroy(self, serializer):
        Product_obj = self.get_object()
        api_key= Product_obj.APIKey.key
        pk= Product_obj.id
        
        delete_doc_rag.apply_async(args= [api_key,pk])  # Call the Celery task
        Product_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class CollectionDocumentMapAPI(APIView):
    """
    API endpoint that returns a mapping of collections to their documents
    """
    
    def get(self,request):
        try:
            rag_obj = ColivaraRAG(collection_name= None )
            list_docs = rag_obj.create_collection_document_map()
            return JsonResponse({
                'status': 'success',   
                'data': list_docs,
            }, status=200)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)
        




#  Assuming you have a function that generates the context based on the query
class ProcessQueryView(APIView):
    serializer_class = QuerySerializer

    def post(self, request, api_key, *args, **kwargs):
        # Extract query_text from request data
        query_text = request.data.get('query_text', '').strip()

        # Validate presence of query_text
        if not query_text:
            return Response(
                {'error': 'query_text is required in the request body.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate API key existence
        try:
            api_key_obj = List_API_Key.objects.get(key=api_key)
        except List_API_Key.DoesNotExist:
            return Response(
                {'error': 'Invalid API key'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Call your function that generates the context
        context = self.process_query(api_key, query_text)

        if not context:
            return Response(
                {'error': 'No images generated from the query'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Process the first item in context
        first_item = context[0]
        metadata = first_item.get('metadata', {})
        base64_img = first_item.get('base64', '')

        # Clean the base64 string if it has a data URI scheme
        if base64_img.startswith('data:image'):
            base64_img = base64_img.split(',')[1]

        try:
            # Decode the base64 image
            image_data = base64.b64decode(base64_img)

            # Create a PIL Image object
            image = PILImage.open(io.BytesIO(image_data))

            # Save image to a BytesIO buffer
            img_io = io.BytesIO()
            image.save(img_io, format='PNG')  # or 'JPEG' if needed
            img_content = ContentFile(img_io.getvalue())
             # Create Query instance
            query_instance = Query.objects.create(
                APIKey=api_key_obj,
                query_text=query_text,
            )

            # Generate filename
            
            filename = f"{str(query_instance.id)}.png"

            
            # Save image to the response_image field
            query_instance.response_image.save(filename, img_content)
            query_instance.save()

            # Build response data
            response_data = {
                'metadata': metadata,
                'image_url': request.build_absolute_uri(query_instance.response_image.url),
                'query_id': query_instance.id,
                'query_text': query_text,
                'created_at': query_instance.created_at
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': f'Error processing image: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def process_query(self, api_key, query_text):
        # Initialize your ColivaraRAG object with the API key
        colivara_obj = ColivaraRAG(collection_name=api_key)
        # Create a message for the query
        messages = [{"role": "user", "content": query_text}]
        # Get the context from the ColivaraRAG object
        context = colivara_obj.draft_response(messages=messages)
        # Return the context
        return context

def get_query_result(request, api_key):
    api_key= "57787b7d-99e8-5a52-abdc-232d2f59e2df"
    colivara_obj= ColivaraRAG(collection_name=api_key)
    messages= {"role": "user", "content": "list all product "},
    context = colivara_obj.draft_response(messages=messages)
    return JsonResponse(context, safe=False)

    
