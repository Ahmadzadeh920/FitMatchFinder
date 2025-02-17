from django.db import models
from accounts.models import List_API_Key
import os 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from PIL import Image as PilImage



def validate_image_format(image):
    valid_formats = ['JPEG', 'PNG', 'GIF', 'BMP', 'TIFF']  # Add any other formats you want to support
    try:
        img = PilImage.open(image)
        if img.format not in valid_formats:
            raise ValidationError(_('Unsupported file format: %(format)s'), params={'format': img.format})
    except Exception as e:
        raise ValidationError(_('Invalid image file: %(error)s'), params={'error': str(e)})

# Create your models here.

class Category(models.Model):
    CategoryId  = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    description = models.TextField()


class Styles(models.Model):
    StyleId  = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField()


class AgeGroup(models.Model):
    AgeGroupId  = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField()



# This function for dynamic path file for collection
def get_upload_path(instance, filename):
    api_key = instance.APIKey.key
    image_id = instance.ImageID
    
    # Create a shorter filename if necessary
    base_filename, file_extension = os.path.splitext(filename)
    max_length = 100  # Set maximum length for filename
    
    # Ensure the combined path length does not exceed the limit
    safe_base_filename = base_filename[:max_length - len(file_extension) - len(str(image_id)) - 1 ]  # Leave space for separator and ID
    
    return os.path.join('Photo_collection', api_key, f"{safe_base_filename}{file_extension}")



class ImageCollection(models.Model): 
    ImageID = models.AutoField(primary_key=True)
    APIKey = models.ForeignKey(List_API_Key, null=False ,  on_delete=models.CASCADE)
    Photo = models.ImageField(upload_to=get_upload_path , validators=[validate_image_format])
    name = models.CharField(max_length=250)
    description = models.TextField()
    Category = models.ForeignKey(Category, null=True ,  on_delete=models.SET_NULL)
    Styles = models.ForeignKey(Styles, null=True ,  on_delete=models.SET_NULL)
    AgeGroup= models.ForeignKey(AgeGroup, null=True,   on_delete=models.SET_NULL)
    Processor_embedded = models.BooleanField(default= False)
   

    
    
    def save(self, *args, **kwargs):
        # Check if this is an update
        if self.pk is not None:
            # Fetch the existing instance to compare the Photo field
            existing_instance = ImageCollection.objects.get(pk=self.pk)
            # If the Photo field has changed, delete the old file
            if existing_instance.Photo != self.Photo:
                if existing_instance.Photo:
                    file_path = existing_instance.Photo.path
                    if os.path.isfile(file_path):
                        os.remove(file_path)  # Delete the old file

        super().save(*args, **kwargs)
        # After saving, update the Photo field's upload path
        if self.Photo and self.Photo.name:
            self.Photo.name = get_upload_path(self,self.Photo.name)
         # Call the original save method to ensure the ImageID is generated
        
       
# this method is called for dlete the exact image file 
    def delete(self, using=None, keep_parents=False):
        # Delete the file associated with this instance
        if self.Photo:
            # Construct the full path to the image file
            file_path = self.Photo.path
            if os.path.isfile(file_path):
                os.remove(file_path)  # Delete the file from the filesystem

        # Call the superclass method to delete the instance
        super().delete(using=using, keep_parents=keep_parents)


    def __str__(self):
        return self.name



class Prompt_API(models.Model): 
    PromptID = models.AutoField(primary_key=True)
    APIKey = models.ForeignKey(List_API_Key, null=False ,  on_delete=models.CASCADE)
    prompt =models.TextField(verbose_name="Prompt", help_text="Enter the prompt text here")
    number_recommended_images = models.IntegerField(default=0)

    def __str__(self):
        return f"PromptAPI {self.PromptID}: {self.prompt[:50]}"  # Display first 50 characters of the prompt