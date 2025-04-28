from django.test import TestCase
from customized_RAG.models import Product, Query
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
        path_file="https://github.com/Ahmadzadeh920/FitMatchFinder/blob/main/core/customized_RAG/tests/test_docs/test_catalogue.pdf"
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
    
    def test_file_deletion_on_model_delete(self):
        product = Product.objects.create(
            APIKey=self.api_key_obj,
            name_file='Test',
            description='Test',
            manual_file=self.test_file
        )
        file_path = product.manual_file.path
        product.delete()
        import os
        self.assertFalse(os.path.exists(file_path))



## Query model test
class QueryModelTest(TestCase):
    def setUp(self):
        # Create a user
        user_obj = CustomUser.objects.create_user(email='testuser2@example.com', password='Password$123', is_verified=True, is_active=True)
        # Create a profile for that user
        profile_obj, created = Profile.objects.get_or_create(
            user=user_obj,
            defaults={
                'first_name': 'Test',
                'last_name': 'User',
                'phone_number': '12345267890'
            }
        )
            
    
    
    # Create List_API_Key linked to profile
        self.api_key_obj = List_API_Key.objects.create(
            profile=profile_obj,
            name_service='Test Service',
            description='Test description'
        )

    def test_create_query(self):
        # Create a Query instance
        query_text = "Sample query"
        query = Query.objects.create(
            APIKey=self.api_key_obj,
            query_text=query_text,
            # response_image can be optional
        )

        # Fetch the query from the database
        fetched_query = Query.objects.get(id=query.id)

        # Assertions
        self.assertEqual(fetched_query.query_text, query_text)
        self.assertEqual(fetched_query.APIKey, self.api_key_obj)
        self.assertIsNotNone(fetched_query.created_at)
        

    def test_str_method(self):
        query_text = "Another test query"
        query = Query.objects.create(
            APIKey=self.api_key_obj,
        
            query_text=query_text,
        )
        self.assertEqual(str(query), query_text)