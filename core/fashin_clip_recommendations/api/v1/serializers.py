from ...models import Category, Styles, AgeGroup,ImageCollection
from rest_framework import serializers



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # or specify fields: ['CategoryId', 'name', 'description']


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Styles
        fields = '__all__'  


class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroup
        fields = '__all__'
        

class ImageCollectionSerializer(serializers.ModelSerializer):
    age_group_name = serializers.CharField(source='AgeGroup.name', read_only=True)
    style_name = serializers.CharField(source='Styles.name', read_only=True)
    category_name = serializers.CharField(source='Category.name', read_only=True)
    
    class Meta:
        model = ImageCollection
        fields = ["ImageID",'Photo', 'name','description', "AgeGroup","age_group_name", "Styles",'style_name', "Category","category_name", "Processor_embedded"]



class PromptAPISerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=255)  


