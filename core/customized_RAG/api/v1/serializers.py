from ...models import Product, Query
from rest_framework import serializers



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name_file','description' , 'manual_file' , 'Processing_boolean']  # or specify fields: ['CategoryId', 'name', 'description']
    

class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name_file', 'description', 'manual_file', 'Processing_boolean']
        extra_kwargs = {
            'name_file': {'required': False , 'max_length': 100},
            'description': {'required': False},
            'manual_file': {'required': False},
            'Processing_boolean': {'required': False},
        }
        
class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = ['id', 'query_text', 'response_image', 'created_at']
        extra_kwargs = {
            
            'response_image': {'required': False},
            'created_at': {'required': False},
            'Processing_boolean': {'required': False},
        }