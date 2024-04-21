from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from registration.schemas import TokensSchema, UserRegisterSchema
from users.models import User


def get_token(user):
    user = User.objects.get(username=user.username)
    access_token = str(AccessToken.for_user(user))
    refresh_token = str(RefreshToken.for_user(user))
    return TokensSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )


def create_user(user_register_schema: UserRegisterSchema):
    user_model = get_user_model()
    user_register_schema.password = make_password(user_register_schema.password)
    user = user_model(**user_register_schema.model_dump())
    user.save()

    return user
