from ...models import Product
from rest_framework import serializers



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description' , 'manual']  # or specify fields: ['CategoryId', 'name', 'description']

