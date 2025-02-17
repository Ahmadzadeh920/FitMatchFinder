from django.urls import path
from django.urls import include
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', CategoryListView)
router.register(r'styles', StyleListView)
router.register(r'AgeGroup', AgeGroupListView)

app_name = "api_v1"
urlpatterns = [
    # registeration_process 
   path('', include(router.urls)),
   path('images/<str:api_key>', ImageCollectionListView.as_view(), name='image-collection-list'),
   path('images/<str:api_key>/<int:pk>', ImageCollectionDetailView.as_view(), name='image-collection-detail'),
   path('chromadb_collection_name' , ChromaDBCollectionsView.as_view(), name='chromadb-collection-name'),
   path('prompt/<str:api_key>', PromptAPIView.as_view(), name='prompt_api_view'),
   #path('test/', test.as_view(), name='tast_fashion_clip'),
]