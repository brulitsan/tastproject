from pydantic import EmailStr, BaseModel


class UserRegisterSchema(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserLoginSchema(BaseModel):
    username: str
    password: str


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str


class ResetChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str