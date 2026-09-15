from sqlalchemy.orm import Session
from datetime import date

from app.services.overview_service import calculate_total_cost,calculate_total_accounts,calculate_average_daily_cost,calculate_overview
from app.services.overview_service import calculate_cost_by_account
from app.services.overview_service import calculate_cost_trend
from app.services.overview_service import calculate_cost_by_service
from app.services.overview_service import calculate_cost_by_environment
from app.services.overview_service import calculate_cost_forecast

# def get_total_cost_controller(db: Session, month:date):

#     total_cost = calculate_total_cost(db, month)

#     return {
#         "month": month,
#         "total_cost": total_cost
#     }


# def get_total_accounts_controller(db: Session, month: date):

#     total_accounts = calculate_total_accounts(db, month)

#     return {
#         "month": month,
#         "total_accounts": total_accounts
#     }



# def get_average_daily_cost_controller(db: Session, month: date):

#     average_daily_cost = calculate_average_daily_cost(db, month)

#     return {
#         "month": month,
#         "average_daily_cost": average_daily_cost
#     }


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