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
    dealer_code: str = Field(
        ...,
        description='Код дилера, состоящий из 5 цифр'
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

    @field_validator('dealer_code')
    @classmethod
    def validate_dealer_code(cls, value):
        if not re.match(r'^\d{5}$', value):
            raise ValueError(
                'Код дилера должен состоять из 5 цифр'
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


class SchemaUserRoleUpdate(BaseModel):
    is_super_admin: bool


class SchemaUserPasswordUpdate(BaseModel):
    old_password: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description='Пароль, от 5 до 50 знаков'
        )
    new_password: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description='Пароль, от 5 до 50 знаков'
        )


class SchemaUserDataUpdate(BaseModel):
    dealer_code: str
    email: EmailStr = Field(
        ...,
        description='Электронная почта'
        )
    phone_number: str = Field(
        ...,
        description='Номер телефона, начинающийся с "+"'
        )


class SchemaUserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    dealer_code: str
    phone_number: str
    is_user: bool
    is_super_admin: bool
