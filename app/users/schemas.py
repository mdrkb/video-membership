from pydantic import BaseModel, EmailStr, SecretStr, validator, root_validator
from app.users.models import User
from app.users import auth


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
    session_id: str = None

    @root_validator
    def validate_user(cls, values):
        err_msg = "Incorrect credentials, please try again."

        email = values.get("email") or None
        password = values.get("password") or None

        if email is None or password is None:
            raise ValueError(err_msg)

        password = password.get_secret_value()

        user_obj = auth.authenticate(email, password)
        if user_obj is None:
            raise ValueError(err_msg)

        token = auth.login(user_obj)
        return {"session_id": token}
