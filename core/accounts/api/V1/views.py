import os
import jwt
from mail_templated import EmailMessage
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .serializer import RegistrationSerializer


from ...tasks import send_validation_email



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
            token = self.get_token_for_user(obj_user)
            validation_link = os.getenv("PASSWORD_ACTIVE_BASE_URL") + str(token)
            # Send the validation email
            send_validation_email.delay(obj_user.email, validation_link)  # Call the Celery task
            return Response(data={"detail": "email send"}, status=status.HTTP_200_OK)
            

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return refresh.access_token
    



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






def send_email(email_address, message):
        send_feedback_email_task.apply_async(args=[
        email_address, message
    ])