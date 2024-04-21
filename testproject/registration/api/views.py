from urllib import request

from django.contrib.auth import authenticate
from django.db import transaction
from drf_yasg.inspectors import ViewInspector
from rest_framework import generics, status, exceptions
from rest_framework.response import Response

from users.models import User
from .serializers import RegisterSerializer, LoginSerializer, ResetChangePasswordSerializer
from ..dependencies import get_token, create_user
from ..exceptions import DifferentPasswordsException
from ..schemas import UserLoginSchema, UserRegisterSchema, ResetChangePasswordSchema


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    inspector_class = ViewInspector

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_schema = UserRegisterSchema.model_validate(serializer.validated_data)
        user = create_user(user_schema)
        token = get_token(user)
        return Response({
            'user': serializer.data,
            'access_token': token.access_token,
            'refresh_token': token.refresh_token
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    inspector_class = ViewInspector

    @transaction.atomic
    def post(self, request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_data = UserLoginSchema(**serializer.validated_data)
        user = authenticate(request, username=user_data.username, password=user_data.password)
        if user is None:
            raise exceptions.AuthenticationFailed("Invalid username or password")

        token = get_token(user)
        return Response(
            {"access_token": token.access_token, "refresh_token": token.refresh_token},
            status=status.HTTP_200_OK,
        )


class ResetChangePasswordView(generics.GenericAPIView):
    serializer_class = ResetChangePasswordSerializer
    inspector_class = ViewInspector

    @transaction.atomic
    def post(self, request) -> Response:
        serializer = self.get_serializer(data=request.data)
        user = self.request.user
        serializer.is_valid(raise_exception=True)

        user_schema = ResetChangePasswordSchema.model_validate(serializer.validated_data)
        if not user.check_password(user_schema.old_password):
            raise DifferentPasswordsException
        user.set_password(user_schema.new_password)
        user.save()

        return Response({'message': 'Password successfully changed'}, status=status.HTTP_201_CREATED)

