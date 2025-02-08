from django.urls import path
from django.urls import include
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'styles', StyleViewSet)
router.register(r'AgeGroup', AgeGroupViewSet)

app_name = "api_v1"
urlpatterns = [
    # registeration_process 
   path('', include(router.urls)),
   path('images/<str:api_key>/', ImageCollectionList.as_view(), name='image-collection-list'),
   path('images/<str:api_key>/<int:pk>/', ImageCollectionDetail.as_view(), name='image-collection-detail'),
   path('chromadb_collection_name/' , ChromaDBCollectionsView.as_view(), name='chromadb-collection-name'),
   path('prompt/<str:api_key>/', PromptAPIView.as_view(), name='prompt'),
   #path('test/', test.as_view(), name='tast_fashion_clip'),
]