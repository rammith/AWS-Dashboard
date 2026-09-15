from datetime import date
from pydantic import BaseModel


class AccountSummaryResponse(BaseModel):
    month: date
    total_accounts: int
    total_monthly_cost: float
    average_monthly_cost_per_account: float


class AccountResponse(BaseModel):
    account_id: str
    account_name: str
    environment: str
    monthly_cost: float
    trend_percentage: float | None
    trend_direction: str