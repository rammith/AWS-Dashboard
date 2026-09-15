from pydantic import BaseModel
from datetime import date


class TotalCostResponse(BaseModel):
    month: date
    total_cost: float


class TotalAccountsResponse(BaseModel):
    month: date
    total_accounts: int


class AverageDailyCostResponse(BaseModel):
    month: date
    average_daily_cost: float


class OverviewResponse(BaseModel):
    month: date
    total_cost: float
    total_accounts: int
    average_daily_cost: float


class CostByAccountResponse(BaseModel):
    account_id: str
    account_name: str
    total_cost: float


class CostByTrendResponse(BaseModel):
    date: date
    total_cost: float


class CostByServiceResponse(BaseModel):
    service: str
    total_cost: float


class CostByEnvironmentResponse(BaseModel):
    environment: str
    total_cost: float


class CostForecastResponse(BaseModel):
    month: date
    forecast_cost: float