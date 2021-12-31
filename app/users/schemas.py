from pydantic import BaseModel, EmailStr, SecretStr, validator
from app.users.models import User


class UserSIgnUpSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    password_confirm: SecretStr

    @validator("email")
    def email_available(cls, email, values, **kwargs):
        q = User.objects.filter(email=email)
        if q.count() != 0:
            raise ValueError("Email is not available")
        return email

    @validator("password_confirm")
    def passwords_match(cls, password_confirm, values, **kwargs):
        password = values.get("password")
        if password != password_confirm:
            raise ValueError("Passwords do not match")
        return password_confirm


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr
