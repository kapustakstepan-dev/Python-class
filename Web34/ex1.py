from pydantic import BaseModel, EmailStr, ValidationError, field_validator


class User(BaseModel):
    username: str
    email: EmailStr

    @field_validator("username")
    @classmethod
    def no_spaces(cls, v: str) -> str:
        if " " in v:
            raise ValueError("Username не повинен містити пробілів")
        return v

try:
    user = User(username="John Doe", email="johndoegmail.com")
except ValidationError as e:
    for error in e.errors():
        print(f"Поле: {error['loc'][0]}")
        print(f"Повідомлення: {error['msg']}")
        print("-" * 20)