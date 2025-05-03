import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class SchemaUserRegister(BaseModel):
    email: EmailStr = Field(
        ...,
        description='Электронная почта'
        )
    password: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description='Пароль, от 5 до 50 знаков'
        )
    phone_number: str = Field(
        ...,
        description='Номер телефона, начинающийся с "+"'
        )
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description='Имя, от 2 до 50 символов'
        )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description='Фамилия, от 2 до 50 символов'
        )

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, value):
        if not re.match(r'^\+\d{11}$', value):
            raise ValueError(
                'Номер телефона должен начинаться с "+"'
                ' и содержать от 1 до 15 цифр'
            )
        return value


class SchemaUserAuth(BaseModel):
    email: EmailStr = Field(
        ...,
        description='Электронная почта'
        )
    password: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description='Пароль, от 5 до 50 знаков'
        )


class ShchemaUserRoleUpdate(BaseModel):
    is_super_admin: bool


class SchemaUserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    is_user: bool
    is_super_admin: bool
