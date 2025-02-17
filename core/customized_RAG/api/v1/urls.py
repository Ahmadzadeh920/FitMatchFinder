from django.urls import path
from django.urls import include
from .views import *

app_name = 'api_v1'

urlpatterns =[
path('ProductListCreate/<str:api_key>' , ProductListView.as_view(), name='product_list_view' )
    
]