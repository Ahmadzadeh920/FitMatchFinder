from django.urls import path
from django.urls import include
from .views import *

app_name = 'api_v1'

urlpatterns =[
path('product/<str:api_key>' , ProductListView.as_view(), name='product_list_create_view' ),
path('product/<str:api_key>/<int:pk>/', ProductDetailView.as_view(), name='product-detail-update'),
path('collection-document-map/', CollectionDocumentMapAPI.as_view(), name='collection_document_map'),
path('api/process-query/<str:api_key>/', ProcessQueryView.as_view(), name='process-query'),
path('process-query-test/<str:api_key>/',get_query_result, name='process-query-test'),
]