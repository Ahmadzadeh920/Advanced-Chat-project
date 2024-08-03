# from django.shortcuts import render


from rest_framework import generics
from .serializers import (RegistrationSerializer,
                           CustomeAuthTokenSerializer,
                           ResetPasswordRequestSerializer,
                           ResetPasswordSerializer,
                           ChangePasswordSerializer)
from ..models import CustomUser, PasswordReset, Profile
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from mail_templated import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from ..utils import EmailThread
from ..permissions import IsVerified
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views.decorators.cache import cache_page
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
            reset_url = os.getenv("PASSWORD_ACTIVE_BASE_URL") + str(token)
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


# this class for login

class ObtainAuthToken_Customized(ObtainAuthToken):
    serializer_class = CustomeAuthTokenSerializer
    
    
    @method_decorator(cache_page(60))
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.id, "email": user.email})


# this class for cutomized logout

class AuthDiscardedToken(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        


# this class for request reseting password
class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        user = CustomUser.objects.filter(email__iexact=email).first()
        serializer.is_valid(raise_exception=True)
        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user) 
            reset = PasswordReset(email=email, token=token)
            reset.save()

            reset_url = os.getenv("PASSWORD_RESET_BASE_URL") +token

            # Sending reset link via email (commented out for clarity)
            data = {
                "subject": "this email for activation for accounts",
                "message": "plase click this linK for reseting password "
                + "<br/> "
                + str(reset_url),
            }
            
            Email_obj = EmailMessage(
                "email/reset_password.tpl",
                data,
                from_email,
                to=[serializer.validated_data["email"]],
            )
            EmailThread(Email_obj).start()
            # ... (email sending code)

            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)
        


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
        

# this class for changing password
class ChangePasswordView(generics.UpdateAPIView):

    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = ChangePasswordSerializer
