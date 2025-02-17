from django.db import models
import os 
# Create your models here.
from django.db import models
from accounts.models import List_API_Key




def get_upload_path(instance, filename):
    api_key = instance.APIKey.key
    image_id = instance.ImageID
    
    # Create a shorter filename if necessary
    base_filename, file_extension = os.path.splitext(filename)
    max_length = 100  # Set maximum length for filename
    
    # Ensure the combined path length does not exceed the limit
    safe_base_filename = base_filename[:max_length - len(file_extension) - len(str(image_id)) - 1 ]  # Leave space for separator and ID
    
    return os.path.join('manual_collection', api_key, f"{safe_base_filename}{file_extension}")



class Product(models.Model):
    id = models.AutoField(primary_key=True)
    API_KEY = models.ForeignKey(List_API_Key, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    manual = models.FileField(upload_to=get_upload_path )

    def __str__(self):
        return self.name