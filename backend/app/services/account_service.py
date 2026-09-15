from sqlalchemy.orm import Session
from datetime import date

from app.dal.account_dal import (
    get_total_accounts,
    get_total_monthly_cost,
    get_accounts_with_cost_and_trend
)


def calculate_account_summary(db: Session, month):

    total_accounts = get_total_accounts(db, month)

    total_monthly_cost = get_total_monthly_cost(db, month)

    if total_accounts > 0:
        average_monthly_cost_per_account = (
            total_monthly_cost / total_accounts
        )
    else:
        average_monthly_cost_per_account = 0

    return {
        "month": month,
        "total_accounts": total_accounts,
        "total_monthly_cost": round(total_monthly_cost, 2),
        "average_monthly_cost_per_account": round(
            average_monthly_cost_per_account, 2
        )
    }



def calculate_accounts(db: Session, month: date):

    accounts = get_accounts_with_cost_and_trend(db, month)

    result = []

    for account in accounts:

        current_cost = account["monthly_cost"]
        previous_cost = account["previous_cost"]

        if previous_cost == 0:

            trend_percentage = None
            trend_direction = "no_previous_data"

        else:

            trend_percentage = (
                (current_cost - previous_cost)
                / previous_cost
            ) * 100

            if trend_percentage > 0:
                trend_direction = "increase"
            elif trend_percentage < 0:
                trend_direction = "decrease"
            else:
                trend_direction = "no_change"

        result.append(
            {
                "account_id": account["account_id"],
                "account_name": account["account_name"],
                "environment": account["environment"],
                "monthly_cost": round(current_cost, 2),
                "trend_percentage": (
                    round(abs(trend_percentage), 2)
                    if trend_percentage is not None
                    else None
                ),
                "trend_direction": trend_direction
            }
        )

    return result