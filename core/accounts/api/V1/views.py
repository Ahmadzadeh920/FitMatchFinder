import os
import jwt
from django.conf import settings
from django.utils import timezone

from mail_templated import EmailMessage
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .serializer import ( RegistrationSerializer ,
                        Customized_TOKEN_OBTAIN_PAIR_SERIALIZER,
                          ResetPasswordRequestSerializer,
                          ResetPasswordSerializer,
                          ChangePasswordSerializer,
                          ProfileSerializer,
                          ListAPIKeySerializer
                          )

from ...tasks import send_validation_email,  send_reset_password_email
from ...models import CustomUser , PasswordReset, List_API_Key
from ...permissions import *

def get_token_for_user(user):
        refresh = RefreshToken.for_user(user)
        return refresh.access_token

class RegisterationApiview(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            obj_user = get_object_or_404(
                CustomUser, email=serializer.validated_data["email"]
            )
            token = get_token_for_user(obj_user)
            validation_link = os.getenv("PASSWORD_ACTIVE_BASE_URL") + str(token)
            # Send the validation email
            send_validation_email.apply_async(args= [obj_user.email, validation_link])  # Call the Celery task
            return Response(data={"detail": "email send"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            


    



class ActivationAccountJWT(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            # decode toke -> id user
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError as e:

            # check_expired_data
            data = {"detail": str(e)}
            return Response(data=data, status=status.HTTP_410_GONE)
        except jwt.exceptions.InvalidSignatureError as e:
            data = {"detail": str(e)}
            return Response(data=data, status=status.HTTP_410_GONE)
        # user_obj
        user_id = decoded_token["user_id"]
        user_obj = get_object_or_404(CustomUser, id=user_id)
        #   CHECK USER_obj is none
        if user_obj.is_verified:
            data = {"detail": "your account has been already verified"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        # is_varified trun to true
        user_obj.is_verified = True
        user_obj.save()
        data = {"detail": "your account is verfied and activated successfully"}
        return Response(data=data, status=status.HTTP_200_OK)
    

# this class for resending Validation Email 
class ResendValidationEmailView(generics.GenericAPIView):
    permission_classes = [AllowAny]  # Allow anyone to access this view
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        
        # Check if the email is provided
        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the user object or return a 404 if not found
        user = get_object_or_404(CustomUser, email=email)

        # Check if the user's account is already verified
        if user.is_verified:
            return Response({"detail": "Your account is already verified."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a new access token for the user
        token = get_token_for_user(user)
        validation_link = os.getenv("PASSWORD_ACTIVE_BASE_URL") + str(token)

        # Send the validation email again
        send_validation_email.apply_async(args=[user.email, validation_link])  # Call the Celery task
        return Response(data={"detail": "Validation email sent."}, status=status.HTTP_200_OK)



# this class for login jwt 
class CustimizedTokenObtainPairView(TokenObtainPairView):
    serializer_class = Customized_TOKEN_OBTAIN_PAIR_SERIALIZER   

# This class for logout jwt 
class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user_obj = CustomUser.objects.filter(email=email).first()
        if not user_obj:
            return Response({"detail": "User with this email is not found"}, status=404)
        else:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user_obj) 
            reset = PasswordReset(email=email, token=token)
            reset.save()
            reset_link = os.getenv("PASSWORD_Reset_BASE_URL") + str(token)
            # Send the validation email
            send_reset_password_email.apply_async(args= [user_obj.email, reset_link])  
        return Response({"detail": "Password reset link has been sent."}, status=200)


# for reseting password
class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = []
    

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        new_password = data['new_password']
        confirm_password = data['confirm_password']
        
        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)
        
        reset_obj = PasswordReset.objects.filter(token=token).first()
        
        if not reset_obj:
            return Response({'error':'Invalid token'}, status=400)
        
        user = CustomUser.objects.filter(email=reset_obj.email).first()
        
        if user:
            user.set_password(request.data['new_password'])
            user.save()
            
            reset_obj.delete()
            
            return Response({'success':'Password updated'})
        else: 
            return Response({'error':'No user found'}, status=404)
        

# Change Password
class ChangePasswordView(generics.UpdateAPIView):

    
    permission_classes = [IsAuthenticated, IsVerified]
    serializer_class = ChangePasswordSerializer
    def get_object(self):
        # Return the user object associated with the request
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

# for updating the profile:
# Update and Retrieve Profile 
class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated, IsVerified]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
    

class ListCreatAPIKeyView(generics.ListCreateAPIView):
    
    serializer_class = ListAPIKeySerializer
    permission_classes = [IsVerified,]

    def get_queryset(self):
        # Return only the API keys for the current user
        return List_API_Key.objects.filter(profile__user=self.request.user)
    def perform_create(self, serializer):
        user = self.request.user
        profile_obj= Profile.objects.filter(user=user).first()
        if profile_obj:      # Set the profile to the current user
            serializer.save(profile=profile_obj)
            return Response({"detail": "This API for this application is created successfully"}, status=status.HTTP_200_OK)
        else: 
            return Response({"detail": "you must first complete your profile to access creation of API"}, status=status.HTTP_200_OK)

class ListAPIKeyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = List_API_Key.objects.all()
    serializer_class = ListAPIKeySerializer
    permission_classes = [IsVerified,]
    def get_queryset(self):
        # Return only the API keys for the current user
        return List_API_Key.objects.filter(profile__user=self.request.user)
    def perform_update(self, serializer):
        # Update the updated_at field to the current timezone
        profile_obj = Profile.objects.get(user=self.request.user)
        serializer.save(updated_at=timezone.now(), profile=profile_obj)
     
    
            