from django.db.models import Q
from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.conf import settings
import os
from celery.result import AsyncResult

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import time
import chromadb
from chromadb.config import Settings
from django.conf import settings as setting_core
from .serializers import *
from ...models import *
from ...tasks import fashion_clip_embedding, fashion_clip_delete, fashion_clip_retrieve, fashion_clip_recommeneder
from ...FashinClip import FashionImageRecommender

from accounts.permissions import IsStaff, IsVerified, IsOwnerOfAPIKey, IsSuperUser
from accounts.models import List_API_Key, Profile, CustomUser


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaff, IsVerified]  # Apply the custom permission



   

class StyleViewSet(viewsets.ModelViewSet):
    queryset = Styles.objects.all()
    serializer_class = StyleSerializer
    permission_classes = [IsStaff, IsVerified]  # Apply the custom permission
   


class AgeGroupViewSet(viewsets.ModelViewSet):
    queryset = AgeGroup.objects.all()
    serializer_class = AgeGroupSerializer
    permission_classes = [IsStaff, IsVerified]  # Apply the custom permission
   

class ImageCollectionList(APIView):
    serializer_class = ImageCollectionSerializer
    permission_classes = [IsVerified , IsOwnerOfAPIKey]  # Apply the custom permission
    def get_queryset(self):
         # Get the currently authenticated user
        user = self.request.user
        api_key = self.kwargs.get('api_key')

        # Use a single query to filter ImageCollection based on the user's profile and associated API keys
        return ImageCollection.objects.filter(
            APIKey__profile__user=user , APIKey__key=api_key
        )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        api_key_value = self.kwargs.get('api_key')

        try:
            # Retrieve the APIKey instance based on the passed api_key
            api_key_obj = List_API_Key.objects.get(key=api_key_value, profile__user=user)
        except List_API_Key.DoesNotExist:
            return Response(data={"detail": "api_key is not valid for this user"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the ImageCollection instance and associate it with the correct APIKey
        serializer.save(APIKey=api_key_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# for the details of imae collectin 
class ImageCollectionDetail(APIView):
    serializer_class = ImageCollectionSerializer
    permission_classes = [IsVerified ,IsOwnerOfAPIKey, ]  #
    def get_object(self, api_key, pk):
        try:
            # Assuming `List_API_Key` is the model that contains the API keys
            user = self.request.user
            api_key_instance = List_API_Key.objects.get(key=api_key , profile__user=user)
          
            return ImageCollection.objects.get(APIKey=api_key_instance, ImageID=pk)
        except List_API_Key.DoesNotExist:
            raise NotFound("API Key not found.")
        except ImageCollection.DoesNotExist:
            raise NotFound("Image collection not found.")

    def get(self, request, api_key, pk):
        image_collection = self.get_object(api_key, pk)
        serializer = ImageCollectionSerializer(image_collection)
        return Response(serializer.data)

    def put(self, request, api_key, pk):
        image_collection = self.get_object(api_key, pk)

        serializer = ImageCollectionSerializer(image_collection, data=request.data)
        if serializer.is_valid():
            previous_Processor_embedded_obj = ImageCollection.objects.get(ImageID=pk)
            updated_image_collection = serializer.save()
            if updated_image_collection.Processor_embedded ==True and previous_Processor_embedded_obj.Processor_embedded== False:
                
                # 
                full_path = updated_image_collection.Photo.path
                # desired_path includes API_Key/name image
                desired_path = "/".join(full_path.split("Photo_collection")[-1:]).lstrip("/") 
                full_image_path = os.path.join(settings.MEDIA_ROOT,"Photo_collection",desired_path)
                
                fashion_clip_embedding.apply_async(args= [api_key, full_image_path, pk])  # Call the Celery task
                # Construct the full image path
                '''fashion_obj = FashionImageRecommender(collection_name=api_key)
               
                preprocess= fashion_obj.load_images(full_image_path,id_img=pk)
                if preprocess:
                
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    error_message = {'it has problem with load image. please check ihe image'}  # Create a dictionary with the error message.
                    return Response(data=error_message, status=status.HTTP_400_BAD_REQUEST)
    '''
            #serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, api_key, pk):
        image_collection = self.get_object(api_key, pk)
        image_collection.delete()
        fashion_clip_delete.apply_async(args= [api_key,pk])  # Call the Celery task
        return Response(status=status.HTTP_204_NO_CONTENT)



class ChromaDBCollectionsView(APIView):
    #permission_classes = [IsSuperUser]  # Apply the custom permission
    def get(self, request):
        try:
            # Initialize ChromaDB client
            chroma_client = chromadb.HttpClient(
                host=setting_core.CHROMA_SERVER_HOST,
                port=setting_core.CHROMA_SERVER_PORT,
                settings=Settings(allow_reset=True, anonymized_telemetry=False)
            )
            
            # Fetch list of collections
            collections = chroma_client.list_collections()
            response_data = {}  # Initialize an empty dictionary
            name = []
            # Extract collection names and IDs
            for collection in collections:
                collection_name = collection.name  
                '''recommender_obj = FashionImageRecommender(collection_name=collection_name)
                ids_img = recommender_obj.retrive_image()
                name.append({collection_name: ids_img})'''
                ids_img_task = fashion_clip_retrieve.apply_async(args=[collection_name])
                
                # Wait for the result (you might want to implement a timeout)
                result = AsyncResult(ids_img_task.id)
                while not result.ready():
                    time.sleep(1)  # Sleep for a while before checking again
                
                ids_img = result.get()  # Assuming this returns a list of IDs
             
                # Convert the IDs to a set and add them to the response dictionary
                # Assuming ids_img is a list, we want to convert it to a set
                response_data[collection_name] = ids_img  # Set ensures unique IDs

            # Return the result in the desired format
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f"An error occurred: {e}")  # Logging the exception
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PromptAPIView(APIView):
   
    def post(self, request, api_key):
        API_obj = List_API_Key.objects.get(key=api_key)
        if API_obj.is_active != True:
            return JsonResponse({'error': 'API key is not active'}, status=400)
      
        serializer = PromptAPISerializer(data=request.data)
        if serializer.is_valid():
            user_description = serializer.data['prompt']
                
             # Schedule the task
            task = fashion_clip_recommeneder.apply_async(args=[api_key, user_description, 5])
            result = AsyncResult(task.id)  # Get the AsyncResult by task ID
            
            # Wait for the task to finish
            while not result.ready():
                time.sleep(1)  # Sleep for a while before checking again
            
            # Retrieve the result
            if result.successful():
                result_recom = result.get()  # This should give you the actual result
                return JsonResponse({"recommendations": result_recom}, status=200)
            else:
                return JsonResponse({"error": "Task failed", "details": str(result.result)}, status=500)
        else:
            return JsonResponse(serializer.errors, status=400)
