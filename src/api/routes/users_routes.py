from typing import TYPE_CHECKING, Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
else:
    Session = Any

from src.core.db import get_db
from src.models.db_models import Accounts, Users
from src.models.schema import AccountAssignment, UserCreate, UserResponse

users_routes = APIRouter(tags=["Usuários"])


@users_routes.get("/users")
async def list_users(db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
    users = db.query(Users).all()
    return JSONResponse(
        status_code=200,
        content={
            "message": "Usuários",
            "data": [UserResponse.model_validate(user).model_dump() for user in users],
        },
    )


@users_routes.get("/users/{user_id}")
async def get_user(
    user_id: int, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return JSONResponse(
        status_code=200,
        content={
            "message": "Usuário encontrado",
            "data": UserResponse.model_validate(user).model_dump(),
        },
    )


@users_routes.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    body: UserCreate, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    existing_user = db.query(Users).filter(Users.cpf == str(body.cpf)).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="CPF já cadastrado")

    user = Users(
        name=body.name,
        age=body.age,
        email=str(body.email),
        cpf=str(body.cpf),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Usuário criado com sucesso",
            "data": UserResponse.model_validate(user).model_dump(),
        },
    )


@users_routes.post("/users/create", status_code=status.HTTP_201_CREATED)
async def create_user_alias(
    body: UserCreate, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    return await create_user(body, db)


@users_routes.post("/users/{user_id}/assign-account")
async def assign_account_to_user(
    user_id: int,
    body: AccountAssignment,
    db: Annotated[Session, Depends(get_db)],
) -> JSONResponse:
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    account = db.query(Accounts).filter(Accounts.id == body.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if account.user_id is not None and account.user_id != user.id:
        raise HTTPException(status_code=409, detail="Conta já pertence a outro usuário")

    if user.account_id is not None and user.account_id != account.id:
        raise HTTPException(status_code=409, detail="Usuário já possui outra conta")

    account.user = user
    db.add(account)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={
            "message": "Conta atribuída com sucesso",
            "data": UserResponse.model_validate(user).model_dump(),
        },
    )
