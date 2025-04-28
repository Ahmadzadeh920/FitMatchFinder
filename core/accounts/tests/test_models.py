from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Profile, List_API_Key, PasswordReset
from django.utils import timezone
import uuid

User = get_user_model()

class UserModelTest(TestCase):

    def setUp(self):
        self.email = "testuser4@example.com"
        self.password = "Testpassword$123"
        self.user = User.objects.create_user(email=self.email, password=self.password)

    def test_create_user(self):
        self.assertEqual(self.user.email, self.email)
        self.assertTrue(self.user.check_password(self.password))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_verified)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email="admin@example.com", password="adminpass")
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_verified)

class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="profileuser@example.com", password="password")
        

    def test_profile_creation(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.first_name, "John")
        self.assertEqual(profile.last_name, "Doe")
        self.assertEqual(profile.phone_number, "1234567890")
        self.assertIn(str(profile), f"{self.user.email} Profile")

    

class ListAPIKeyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="apikeyuser@example.com", password="password")
        self.profile = Profile.objects.get(
            user=self.user,
            
        )
        self.api_key = List_API_Key.objects.create(
            profile=self.profile,
            name_service="Test Service",
            description="Test description"
        )

    def test_generate_uuid(self):
        uuid_str = List_API_Key.generate_uuid()
        self.assertIsInstance(uuid_str, str)
        self.assertTrue(uuid.UUID(uuid_str))  # Should not raise error

    def test_create_api_key(self):
        self.assertEqual(self.api_key.profile, self.profile)
        self.assertEqual(self.api_key.name_service, "Test Service")
        self.assertTrue(self.api_key.is_active)
        self.assertIn(self.api_key.key, self.api_key.__str__())

class PasswordResetModelTest(TestCase):

    def setUp(self):
        self.email = "resetuser@example.com"
        self.token = "somerandomtoken"
        self.pw_reset = PasswordReset.objects.create(
            email=self.email,
            token=self.token
        )

    def test_password_reset_fields(self):
        self.assertEqual(self.pw_reset.email, self.email)
        self.assertEqual(self.pw_reset.token, self.token)
        self.assertIsInstance(self.pw_reset.created_at, timezone.datetime)

# Note: For more comprehensive tests, consider testing model methods, validation,
# and signals more thoroughly.
