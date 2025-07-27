from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import List_API_Key, CustomUser, Profile
from AI_chat_bot.models import Reference, ChatBotQA
from AI_chat_bot.api.v1.serializers import ReferenceSerializer, ChatBotQASerializer


class ReferenceSerializerTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(email='testuser@example.com', password='Password$123', is_verified=True)
        profile = Profile.objects.create(user=user, first_name='Test', last_name='User', phone_number='1234567890')
        self.api_key = List_API_Key.objects.create(profile=profile, name_service="Test", description="Test")

    def test_valid_pdf_file(self):
        file = SimpleUploadedFile("file.pdf", b"%PDF-1.4 test content", content_type="application/pdf")
        data = {'API_Key': self.api_key.id, 'reference_doc': file}
        serializer = ReferenceSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_file_extension(self):
        file = SimpleUploadedFile("file.txt", b"Not a PDF", content_type="text/plain")
        data = {'API_Key': self.api_key.id, 'reference_doc': file}
        serializer = ReferenceSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('reference_doc', serializer.errors)
        self.assertEqual(str(serializer.errors['reference_doc'][0]), "Only PDF files are allowed.")


class ChatBotQASerializerTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(email='testuser@example.com', password='Password$123', is_verified=True)
        profile = Profile.objects.create(user=user, first_name='Test', last_name='User', phone_number='1234567890')
        self.api_key = List_API_Key.objects.create(profile=profile, name_service="Test", description="Test")

    def test_valid_serialization(self):
        qa = ChatBotQA.objects.create(
            API_Key=self.api_key,
            question="What is Python?",
            response="Python is a programming language."
        )
        serializer = ChatBotQASerializer(instance=qa)
        data = serializer.data
        self.assertEqual(data['question'], "What is Python?")
        self.assertEqual(data['response'], "Python is a programming language.")
        self.assertEqual(data['API_Key'], self.api_key.id)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

    def test_deserialization(self):
        data = {
            'API_Key': self.api_key.id,
            'question': "What is AI?",
            'response': "Artificial Intelligence"
        }
        serializer = ChatBotQASerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        self.assertEqual(instance.question, "What is AI?")
