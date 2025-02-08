from rest_framework import permissions
from .models import Profile, List_API_Key

class IsVerified(permissions.BasePermission):
    message = 'This account is not verfied. Please verify Now'

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_verified
    


class IsCompeletedProfile(permissions.BasePermission):
    message = 'Your profile is not completed. Please complete it Now'

    def has_object_permission(self, request, view):
        user = request.user
        profile_obj = Profile.objects.get(user=user)
        if profile_obj.first_name and profile_obj.last_name and profile_obj.phone_number:
            return True 
        
        return False
    


class IsStaff(permissions.BasePermission):
    message = 'This account is not setting as staff. you do not have permission'

    def has_permission(self, request, view):
        user = request.user
        return  user.is_staff
    
class IsSuperUser(permissions.BasePermission):
    message = 'This account is not setting as superuser. you do not have permission'

    def has_permission(self, request, view):
        user = request.user
        return  user.is_superuser

class IsOwnerOfAPIKey(permissions.BasePermission):
    """
    Custom permission to only allow owners of an API key to access it.
    """

    def has_permission(self, request, view):
        # First, check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if an API key is provided in the request by the get method
        api_key = view.kwargs.get('api_key') # Adjust this depending on how you send the API key

        if api_key is None:
            return False  # No API key provided

        # Check if the API key belongs to the user
        try:
            api_key_object = List_API_Key.objects.get(key=api_key, profile__user=request.user)
            return api_key_object.is_active  # You may want to check if the key is active
        except List_API_Key.DoesNotExist:
            return False  # API key does not exist or does not belong to the user

        return False
