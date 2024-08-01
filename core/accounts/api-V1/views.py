# from django.shortcuts import render


from rest_framework import generics
from .serializers import RegistrationSerializer
from ..models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.permissions import IsAuthenticated, AllowAny
from mail_templated import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from ..utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
import os
# Create your views here.
from_email = os.getenv('From_email')

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
            reset_url = settings.PASSWORD_ACTIVE_BASE_URL + str(token)
            data = {
                "subject": "this email for activation for accounts",
                "message": "plase click this linK for activation of account "
                + "<br/> "
                + str(reset_url),
            }
            
            Email_obj = EmailMessage(
                "email/activation_accounts.tpl",
                data,
                from_email,
                to=[serializer.validated_data["email"]],
            )
            EmailThread(Email_obj).start()

            return Response(data={"detail": "email send"}, status=status.HTTP_200_OK)
        return Response(
            status=status.HTTP_400_BAD_REQUEST, data={"data": serializer.errors}
        )

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return refresh.access_token

    
 # for activating accounts   
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






