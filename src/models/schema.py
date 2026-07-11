from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic_br import CPF  # noqa: TC002


class UserCreate(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(gt=0)
    email: EmailStr
    cpf: CPF


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    email: str
    cpf: str
    account_id: int | None = None


class AccountCreate(BaseModel):
    agency: str = Field(min_length=1)
    user_id: int | None = None


class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    agency: str
    user_id: int | None = None


class AccountAssignment(BaseModel):
    account_id: int
