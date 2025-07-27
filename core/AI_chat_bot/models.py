# models.py
from django.db import models
from accounts.models import List_API_Key
from django.core.exceptions import ValidationError
import os

def validate_pdf(value):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != '.pdf':
        raise ValidationError("Only PDF files are allowed.")
    

def get_upload_path(instance, filename):
    try:
        api_key = instance.API_Key.key
    except Exception:  # Catches both DoesNotExist and None cases
        api_key = 'no_api_key'
    
    return os.path.join('Refrence_AI_chat_bot', api_key, filename)




class Reference(models.Model):
    API_Key = models.ForeignKey(List_API_Key, on_delete=models.CASCADE)
    reference_doc = models.FileField(upload_to=get_upload_path, validators=[validate_pdf])

    def __str__(self):
        return f"Reference for {self.API_Key}"



class ChatBotQA(models.Model):
    API_Key = models.ForeignKey(List_API_Key, on_delete=models.CASCADE)
    question = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # set once when created
    updated_at = models.DateTimeField(auto_now=True)      # updates every save

    def __str__(self):
        # Show a snippet of the question for easy identification
        return self.question[:50] + ("..." if len(self.question) > 50 else "")