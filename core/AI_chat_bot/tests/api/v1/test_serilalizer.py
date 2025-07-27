import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from AI_chat_bot.models import Reference
from AI_chat_bot.api.v1.serializers import ReferenceSerializer
from accounts.models import List_API_Key  # your FK model

