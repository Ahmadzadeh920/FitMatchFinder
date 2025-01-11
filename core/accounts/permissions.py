from rest_framework import permissions
from .models import Profile

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
    
