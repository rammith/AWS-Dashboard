from sqlalchemy.orm import Session
from sqlalchemy import func

from datetime import date

from app.models.monthly_cost import MonthlyCost
from app.models.account_environment import AccountEnvironment


# API 1: Get total accounts and total monthly cost for a given month
def get_total_accounts(db: Session, month):

    total_accounts = (
        db.query(
            func.count(func.distinct(MonthlyCost.account_id))
        )
        .filter(
            MonthlyCost.month_start == month
        )
        .scalar()
    )

    return total_accounts or 0


def get_total_monthly_cost(db: Session, month):

    total_monthly_cost = (
        db.query(
            func.sum(MonthlyCost.total_costs)
        )
        .filter(
            MonthlyCost.month_start == month
        )
        .scalar()
    )

    return total_monthly_cost or 0





# API 2: Get accounts with their monthly cost and trend compared to the previous month
def get_accounts_with_cost_and_trend(db: Session, month: date):

    if month.month == 1:
        previous_month = date(month.year - 1, 12, 1)
    else:
        previous_month = date(month.year, month.month - 1, 1)

    current_data = (
        db.query(
            AccountEnvironment.account_id,
            AccountEnvironment.account_name,
            AccountEnvironment.environment,
            MonthlyCost.total_costs.label("monthly_cost")
        )
        .join(
            MonthlyCost,
            AccountEnvironment.account_id == MonthlyCost.account_id
        )
        .filter(
            MonthlyCost.month_start == month
        )
        .all()
    )

    previous_data = (
        db.query(
            MonthlyCost.account_id,
            MonthlyCost.total_costs.label("previous_cost")
        )
        .filter(
            MonthlyCost.month_start == previous_month
        )
        .all()
    )

    previous_costs = {
        row.account_id: row.previous_cost or 0
        for row in previous_data
    }

    return [
        {
            "account_id": row.account_id,
            "account_name": row.account_name,
            "environment": row.environment,
            "monthly_cost": row.monthly_cost or 0,
            "previous_cost": previous_costs.get(row.account_id, 0)
        }
        for row in current_data
    ]