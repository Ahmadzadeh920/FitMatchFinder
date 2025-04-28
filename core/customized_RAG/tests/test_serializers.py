# test_serializers.py
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from customized_RAG.models import Product, Query
from accounts.models import List_API_Key, CustomUser, Profile
from customized_RAG.api.v1.serializers import (
    ProductSerializer,
    ProductUpdateSerializer,
    QuerySerializer
)
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
import datetime


path_file="https://github.com/Ahmadzadeh920/FitMatchFinder/blob/main/core/customized_RAG/tests/test_docs/test_catalogue.pdf"
updated_path_file="https://github.com/Ahmadzadeh920/FitMatchFinder/blob/main/core/customized_RAG/tests/test_docs/updated_catalogue.pdf"
image_path_file="https://github.com/Ahmadzadeh920/FitMatchFinder/blob/main/core/customized_RAG/tests/test_docs/responce_example.png"


class ProductSerializerTest(TestCase):
    def setUp(self):
        # Create a user
        user_obj = CustomUser.objects.create_user(email='testuser3@example.com', password='Password$123', is_verified=True, is_active=True)
        # Create a profile for that user
        profile_obj, created = Profile.objects.get_or_create(
            user=user_obj,
            defaults={
                'first_name': 'Test_3',
                'last_name': 'User3',
                'phone_number': '123452678903'
            }
        )
            
    
    # Create List_API_Key linked to profile
        self.api_key_obj = List_API_Key.objects.create(
            profile=profile_obj,
            name_service='Test Service',
            description='Test description'
        )

        
        self.product_data = {
            'name_file': 'Test Product',
            'description': 'This is a test product',
            'manual_file': SimpleUploadedFile(path_file, b"file_content"),
            'Processing_boolean': False,
            'APIKey': self.api_key_obj.id  # Assuming you want to set the APIKey here
        }


    def test_product_serializer_valid_data(self):
        serializer = ProductSerializer(data=self.product_data)
        self.assertTrue(serializer.is_valid())
        serializer.validated_data['APIKey']= self.api_key_obj 
        product = serializer.save()
        self.assertEqual(product.name_file, 'Test Product')
        self.assertEqual(product.description, 'This is a test product')
        self.assertEqual(product.Processing_boolean, False)
        self.assertTrue(product.manual_file.name.endswith('test_catalogue.pdf'))

    def test_product_serializer_missing_required_fields(self):
        # Test missing name_file (required field)
        invalid_data = self.product_data.copy()
        invalid_data.pop('name_file')
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name_file', serializer.errors)

        # Test missing description (required field)
        invalid_data = self.product_data.copy()
        invalid_data.pop('description')
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)

    def test_product_serializer_max_length(self):
        # Test name_file max length (assuming it's 100 based on update serializer)
        invalid_data = self.product_data.copy()
        invalid_data['name_file'] = 'ass' * 100 # Assuming max_length is 250
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name_file', serializer.errors)

    def test_product_serializer_output(self):
        product = Product.objects.create(
            name_file='Test Output',
            description='Output test',
            manual_file=SimpleUploadedFile("output.pdf", b"output_content"),
            Processing_boolean=True,
            APIKey=  self.api_key_obj
        )
        serializer = ProductSerializer(product)
        expected_fields = ['id', 'name_file', 'description', 'manual_file', 'Processing_boolean']
        self.assertEqual(set(serializer.data.keys()), set(expected_fields))
        self.assertEqual(serializer.data['name_file'], 'Test Output')
        self.assertEqual(serializer.data['description'], 'Output test')
        self.assertTrue(serializer.data['manual_file'].endswith('output.pdf'))
        self.assertEqual(serializer.data['Processing_boolean'], True)



# class ProductUpdateSerializerTest


class ProductUpdateSerializerTest(TestCase):
    def setUp(self):
         # Create a user
        user_obj = CustomUser.objects.create_user(email='testuser4@example.com', password='Password$123', is_verified=True, is_active=True)
        # Create a profile for that user
        profile_obj, created = Profile.objects.get_or_create(
            user=user_obj,
            defaults={
                'first_name': 'Test_4',
                'last_name': 'User4',
                'phone_number': '123452678903'
            }
        )
            
    
    # Create List_API_Key linked to profile
        self.api_key_obj = List_API_Key.objects.create(
            profile=profile_obj,
            name_service='Test Service',
            description='Test description'
        )

        
      
        self.product = Product.objects.create(
            name_file='Original Name',
            description='Original Description',
            manual_file=SimpleUploadedFile(path_file, b"original_content"),
            Processing_boolean=False,
            APIKey =self.api_key_obj  # Assuming you want to set the APIKey here
        )
        self.update_data = {
            'name_file': 'Updated Name',
            'description': 'Updated Description',
            'manual_file': SimpleUploadedFile(updated_path_file, b"updated_content"),
            'Processing_boolean': True
        }

    def test_product_update_serializer_partial_update(self):
        # Test that fields can be updated individually
        serializer = ProductUpdateSerializer(
            instance=self.product,
            data={'name_file': 'Partial Update'},
            partial=True
        )
        self.assertTrue(serializer.is_valid())
        updated_product = serializer.save()
        self.assertEqual(updated_product.name_file, 'Partial Update')
        self.assertEqual(updated_product.description, 'Original Description')  # unchanged

    def test_product_update_serializer_all_fields_optional(self):
        # Test that all fields are optional
        for field in ['name_file', 'description', 'manual_file', 'Processing_boolean']:
            serializer = ProductUpdateSerializer(
                instance=self.product,
                data={},
                partial=True
            )
            self.assertTrue(serializer.is_valid())

    def test_product_update_serializer_full_update(self):
        serializer = ProductUpdateSerializer(
            instance=self.product,
            data=self.update_data
        )
        self.assertTrue(serializer.is_valid())
        updated_product = serializer.save()
        
        self.assertEqual(updated_product.name_file, 'Updated Name')
        self.assertEqual(updated_product.description, 'Updated Description')
        self.assertTrue(updated_product.manual_file.name.endswith('updated_catalogue.pdf'))
        self.assertEqual(updated_product.Processing_boolean, True)

    def test_product_update_serializer_max_length(self):
        # Test name_file max length enforcement
        invalid_data = self.update_data.copy()
        invalid_data['name_file'] = 'ass' * 100
        serializer = ProductUpdateSerializer(
            instance=self.product,
            data=invalid_data
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('name_file', serializer.errors)



class QuerySerializerTest(TestCase):
    def setUp(self):
        # Create a user
        user_obj = CustomUser.objects.create_user(email='testuser5@example.com', password='Password$123', is_verified=True, is_active=True)
        # Create a profile for that user
        profile_obj, created = Profile.objects.get_or_create(
            user=user_obj,
            defaults={
                'first_name': 'Test_5',
                'last_name': 'User5',
                'phone_number': '123452678903'
            }
        )
            
    
    # Create List_API_Key linked to profile
        self.api_key_obj = List_API_Key.objects.create(
            profile=profile_obj,
            name_service='Test Service',
            description='Test description'
        )

        self.query_data = {
            'query_text': 'Test query',
            'response_image': SimpleUploadedFile(image_path_file, b"image_content"),
            'APIKey': self.api_key_obj.id  # Pass the primary key
           
        }

    def test_query_serializer_valid_data(self):
        serializer = QuerySerializer(data=self.query_data)
        if not serializer.is_valid():
            print(serializer.errors)  # For debugging
        self.assertTrue(serializer.is_valid())
        
        
        query = serializer.save()
        self.assertEqual(query.query_text, 'Test query')
        self.assertTrue(query.response_image.name.endswith('test.jpg'))
        self.assertIsNotNone(query.created_at)
