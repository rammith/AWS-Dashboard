from sqlalchemy.orm import Session
from datetime import date

from app.services.overview_service import calculate_overview
from app.services.overview_service import calculate_cost_by_account
from app.services.overview_service import calculate_cost_trend
from app.services.overview_service import calculate_cost_by_service
from app.services.overview_service import calculate_cost_by_environment
from app.services.overview_service import calculate_cost_forecast



def get_overview_controller(db: Session, month: date):

    return calculate_overview(db, month)


def get_cost_by_account_controller(db: Session, month: date):

    return calculate_cost_by_account(db, month)


def get_cost_trend_controller(db: Session, month: date):

    return calculate_cost_trend(db, month)


def get_cost_by_service_controller(db: Session, month: date):

    return calculate_cost_by_service(db, month)


def get_cost_by_environment_controller(db: Session, month):

    return calculate_cost_by_environment(db, month)


def get_cost_forecast_controller(db: Session, month: date):
    return calculate_cost_forecast(db, month)