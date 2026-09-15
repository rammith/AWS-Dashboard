from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.controllers.overview_controller import get_overview_controller,get_cost_by_account_controller
from app.controllers.overview_controller import get_cost_trend_controller
from app.controllers.overview_controller import get_cost_by_service_controller
from app.controllers.overview_controller import (
    get_cost_by_environment_controller,
    get_cost_forecast_controller
)

from app.schemas.overview import (
    OverviewResponse,
    CostByAccountResponse,
    CostByTrendResponse,
    CostByServiceResponse,
    CostByEnvironmentResponse,
    CostForecastResponse)

from datetime import date


router = APIRouter(
    prefix="/api/overview",
    tags=["Overview"]
)


# @router.get("/total-cost", response_model=TotalCostResponse)
# def get_total_cost(
#     month: date,
#     db: Session = Depends(get_db)
# ):
#     return get_total_cost_controller(db, month)


# @router.get("/total-accounts", response_model=TotalAccountsResponse)
# def get_total_accounts(
#     month: date,
#     db: Session = Depends(get_db)
# ):
#     return get_total_accounts_controller(db, month)


# @router.get("/average-daily-cost",response_model=AverageDailyCostResponse)
# def get_average_daily_cost(
#     month: date,
#     db: Session = Depends(get_db)
# ):
#     return get_average_daily_cost_controller(db, month)


@router.get("/total", response_model=OverviewResponse)
def get_overview(
    month: date,
    db: Session = Depends(get_db)
):
    return get_overview_controller(db, month)


@router.get("/cost-by-account",response_model=list[CostByAccountResponse])
def get_cost_by_account(
    month: date,
    db: Session = Depends(get_db)
):
    return get_cost_by_account_controller(db, month)


@router.get("/cost_trend", response_model=list[CostByTrendResponse])
def get_cost_trend(
    month: date,
    db: Session = Depends(get_db)
):
    return get_cost_trend_controller(db,month)


@router.get("/cost_by_service",response_model=list[CostByServiceResponse])
def get_cost_by_service(
    month: date,
    db: Session = Depends(get_db)
):
    return get_cost_by_service_controller(db, month)


@router.get("/cost_by_environment",response_model=list[CostByEnvironmentResponse])
def get_cost_by_environment(
    month: date,
    db: Session = Depends(get_db)
):
    return get_cost_by_environment_controller(db, month)


@router.get("/cost_forecast", response_model=CostForecastResponse)
def get_cost_forecast(
    month: date,
    db: Session = Depends(get_db)
):
    return get_cost_forecast_controller(db, month)