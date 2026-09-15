from datetime import date
from sqlalchemy.orm import Session

from app.services.account_service import (
    calculate_account_summary,
    calculate_accounts
)


def get_account_summary_controller(
    db: Session,
    month: date
):
    return calculate_account_summary(db, month)


def get_accounts_controller(
    db: Session,
    month: date
):
    return calculate_accounts(db, month)