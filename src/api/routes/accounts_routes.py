from typing import TYPE_CHECKING, Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
else:
    Session = Any

from src.core.db import get_db
from src.models.db_models import Accounts, Users
from src.models.schema import AccountCreate, AccountResponse

accounts_routes = APIRouter(tags=["Contas"])


@accounts_routes.get("/accounts")
async def list_accounts(db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
    accounts = db.query(Accounts).all()
    return JSONResponse(
        status_code=200,
        content={
            "message": "Contas",
            "data": [
                AccountResponse.model_validate(account).model_dump()
                for account in accounts
            ],
        },
    )


@accounts_routes.get("/accounts/{account_id}")
async def get_account(
    account_id: int, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    account = db.query(Accounts).filter(Accounts.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    return JSONResponse(
        status_code=200,
        content={
            "message": "Conta encontrada",
            "data": AccountResponse.model_validate(account).model_dump(),
        },
    )


@accounts_routes.post("/accounts", status_code=status.HTTP_201_CREATED)
async def create_account(
    body: AccountCreate, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    if body.user_id is not None:
        user = db.query(Users).filter(Users.id == body.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        if user.account_id is not None:
            raise HTTPException(status_code=409, detail="Usuário já possui uma conta")

    account = Accounts(agency=body.agency)
    if body.user_id is not None:
        account.user_id = body.user_id

    db.add(account)
    db.commit()
    db.refresh(account)

    if body.user_id is not None:
        user = db.query(Users).filter(Users.id == body.user_id).first()
        account.user = user
        db.add(account)
        db.commit()
        db.refresh(account)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Conta criada com sucesso",
            "data": AccountResponse.model_validate(account).model_dump(),
        },
    )


@accounts_routes.post("/accounts/create", status_code=status.HTTP_201_CREATED)
async def create_account_alias(
    body: AccountCreate, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    return await create_account(body, db)
