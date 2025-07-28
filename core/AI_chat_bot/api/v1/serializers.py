from rest_framework import serializers
from AI_chat_bot.models import Reference, ChatBotQA

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['API_Key', 'reference_doc']

    def validate_reference_doc(self, file):
        if not file.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        return file
    


class ChatBotQASerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBotQA
        fields = ['id', 'API_Key', 'question', 'response', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']