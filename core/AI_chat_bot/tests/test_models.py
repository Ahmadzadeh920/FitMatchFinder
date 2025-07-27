from django.test import TestCase
from AI_chat_bot.models import Reference, ChatBotQA
from accounts.models import List_API_Key, CustomUser, Profile
from django.core.files.uploadedfile import SimpleUploadedFile

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        # Create a user
        user_obj = CustomUser.objects.create_user(email='testuser@example.com', password='Password$123', is_verified=True, is_active=True)
        # Create a profile for that user
        profile_obj, created = Profile.objects.get_or_create(
            user=user_obj,
            defaults={
                'first_name': 'Test',
                'last_name': 'User',
                'phone_number': '1234567890'
            }
        )
            
    
    
    # Create List_API_Key linked to profile
        cls.api_key_obj = List_API_Key.objects.create(
            profile=profile_obj,
            name_service='Test Service',
            description='Test description'
        )
        path_file="https://github.com/Ahmadzadeh920/FitMatchFinder/blob/main/core/AI_chat_bot/tests/test_docs/test_catalogue.pdf"
        cls.test_file = SimpleUploadedFile(path_file, b"file_content")
    
    def test_reference_creation(self):
        reference = Reference.objects.create(
            API_Key=self.api_key_obj,
            reference_doc=self.test_file
        )
        self.assertEqual(reference.API_Key, self.api_key_obj)
        self.assertTrue(reference.reference_doc.name.startswith("Refrence_AI_chat_bot/"+self.api_key_obj.key+"/"))
        self.assertIn("Reference for", str(reference))


    def test_chatbot_qa_creation(self):
        qa = ChatBotQA.objects.create(
            API_Key=self.api_key_obj,
            question="What is the capital of France?",
            response="The capital of France is Paris."
        )
        self.assertEqual(qa.API_Key, self.api_key_obj)
        self.assertEqual(qa.question, "What is the capital of France?")
        self.assertEqual(qa.response, "The capital of France is Paris.")
        self.assertIsNotNone(qa.created_at)
        self.assertIsNotNone(qa.updated_at)
        self.assertIn("What is the capital", str(qa))