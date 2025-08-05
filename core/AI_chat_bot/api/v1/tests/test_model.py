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
    
    def test_product_creation(self):
        product = Product.objects.create(
            APIKey=self.api_key_obj,
            name_file='Test Product',
            description='Test Description',
            manual_file=self.test_file
        )
        self.assertEqual(str(product), 'Test Product')
        self.assertTrue(product.manual_file.name.startswith("manual_collection/"+self.api_key_obj.key+"/"))
 