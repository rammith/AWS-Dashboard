from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.account import AccountSummaryResponse, AccountResponse
from app.controllers.account_controller import (
    get_account_summary_controller,
    get_accounts_controller
)


router = APIRouter(
    prefix="/api/accounts",
    tags=["Accounts"]
)


@router.get("/summary",response_model=AccountSummaryResponse)
def get_account_summary(
    month: date,
    db: Session = Depends(get_db)
):
    return get_account_summary_controller(db, month)


@router.get("",response_model=list[AccountResponse])
def get_accounts(
    month: date,
    db: Session = Depends(get_db)
):
    return get_accounts_controller(db, month)