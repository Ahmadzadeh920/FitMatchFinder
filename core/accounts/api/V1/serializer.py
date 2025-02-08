import re
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core import exceptions
from ...models import CustomUser, Profile, List_API_Key

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        # Check if passwords match
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail": "Passwords do not match."})

        # Validate password complexity
        password = attrs.get("password")
        self.validate_password_complexity(password)

        # Validate password using Django's built-in validator
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)

    def validate_password_complexity(self, password):
        # Check minimum length
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")

        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")

        # Check for at least one symbol
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise serializers.ValidationError("Password must contain at least one special character.")

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return CustomUser.objects.create_user(**validated_data)
    

# Login serializer
class Customized_TOKEN_OBTAIN_PAIR_SERIALIZER(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"details": "user is not verified"})
        validated_data["email"] = self.user.email
        validated_data["user_id"] = self.user.id
        return validated_data

#  for reset password
class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.RegexField(
        regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        write_only=True,
        error_messages={'invalid': ('Password must be at least 8 characters long with at least one capital letter and symbol')})
    confirm_password = serializers.CharField(write_only=True, required=True)


# this serializer for changing password
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:

            serializers.ValidationError({"Password": list(e.messages)})

        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data["password"])
        instance.save()

        return instance
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'profile_picture', 'phone_number']
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Check if the instance is provided; if it is, we are updating
            if self.instance:
                # Make 'profile_picture' optional during updates
                self.fields['profile_picture'].required = False
                # Optionally, you can also set other fields as required if needed
                self.fields['first_name'].required = True
                self.fields['last_name'].required = True
                self.fields['phone_number'].required = True

    def validate(self, attrs):
        # Add any additional validation logic if necessary
        return super().validate(attrs)


# this serializer is for List API Key 
class ListAPIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = List_API_Key
        fields = ['id','key', 'created_at', 'updated_at', 'is_active', 'name_service', 'description']
        read_only_fields = ['key', 'created_at', 'updated_at', 'is_active']  # Make key read-only Specify only the fields to expose