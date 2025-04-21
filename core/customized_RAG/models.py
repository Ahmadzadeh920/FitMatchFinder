from django.db import models
import os
from accounts.models import List_API_Key

def get_upload_path(instance, filename):
    try:
        api_key = instance.APIKey.key
    except Exception:  # Catches both DoesNotExist and None cases
        api_key = 'no_api_key'
    '''
    id = instance.id
    base_filename, file_extension = os.path.splitext(filename)
    max_length = 100
    safe_base_filename = base_filename[:max_length - len(file_extension) - len(str(id)) - 1]
    
    return os.path.join('manual_collection', api_key, f"{safe_base_filename}{file_extension}")
'''
    return os.path.join('manual_collection', api_key, filename)


def get_upload_path_response(instance, filename):
    try:
        api_key = instance.APIKey.key
        
    except Exception:  # Catches both DoesNotExist and None cases
        api_key = 'no_api_key'
   
    return os.path.join('response_collection', api_key, filename)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    APIKey = models.ForeignKey(List_API_Key, null=False ,  on_delete=models.CASCADE)
    name_file = models.CharField(max_length=255)
    description = models.TextField()
    manual_file = models.FileField(upload_to=get_upload_path)
    Processing_boolean = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        # Handle old file deletion if updating
        if self.pk is not None:
            existing_instance = Product.objects.get(pk=self.pk)
            if existing_instance.manual_file != self.manual_file:
                if existing_instance.manual_file:
                    file_path = existing_instance.manual_file.path
                    if os.path.isfile(file_path):
                        os.remove(file_path)

        # Let Django handle the path automatically via upload_to
        super().save(*args, **kwargs)
        
       
# this method is called for dlete the exact image file 
    def delete(self, using=None, keep_parents=False):
        # Delete the file associated with this instance
        if self.manual_file:
            # Construct the full path to the image file
            file_path = self.manual_file.path
            if os.path.isfile(file_path):
                os.remove(file_path)  # Delete the file from the filesystem

        # Call the superclass method to delete the instance
        super().delete(using=using, keep_parents=keep_parents)


    def __str__(self):
        return self.name




class Query(models.Model):
    id = models.AutoField(primary_key=True)
    APIKey = models.ForeignKey(List_API_Key, null=False ,  on_delete=models.CASCADE)
    query_text = models.TextField()
    response_image = models.ImageField(upload_to=get_upload_path_response, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.query_text