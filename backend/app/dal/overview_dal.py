from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.monthly_cost import MonthlyCost
from app.models.daily_cost import DailyCost
from app.models.account_environment import AccountEnvironment

from datetime import date, datetime, time


# 1 API
def get_total_cost(db: Session, month):

    month_start = datetime.combine(month, time.min)

    total_cost = (
        db.query(func.sum(MonthlyCost.total_costs))
        .filter(MonthlyCost.month_start == month)
        .scalar()
    )

    return total_cost or 0



# 1 API
def get_total_accounts(db: Session, month: date):

    total_accounts = (
        db.query(func.count(func.distinct(MonthlyCost.account_id)))
        .filter(MonthlyCost.month_start == month)
        .scalar()
    )

    return total_accounts or 0



# 1 API
def get_average_daily_cost(db: Session, month: date):

    start_date = datetime.combine(month, time.min)

    if month.month == 12:
        next_month = date(month.year + 1, 1, 1)
    else:
        next_month = date(month.year, month.month + 1, 1)

    end_date = datetime.combine(next_month, time.min)

    daily_totals = (
        db.query(
            DailyCost.date,
            func.sum(DailyCost.total_costs).label("daily_total")
        )
        .filter(
            DailyCost.date >= start_date,
            DailyCost.date < end_date
        )
        .group_by(DailyCost.date)
        .subquery()
    )

    average_daily_cost = (
        db.query(func.avg(daily_totals.c.daily_total))
        .scalar()
    )

    return average_daily_cost or 0


# 2 API
def get_cost_by_account(db: Session, month: date):

    month_start = datetime.combine(month, time.min)

    cost_by_account = (
        db.query(
            MonthlyCost.account_id,
            MonthlyCost.account_name,
            MonthlyCost.total_costs
        )
        .filter(
            MonthlyCost.month_start == month_start
        )
        .all()
    )

    return cost_by_account



# 3 API
def get_cost_trend(db: Session, month: date):

    start_date = datetime.combine(month, time.min)

    if month.month == 12:
        next_month = date(month.year + 1, 1, 1)
    else:
        next_month = date(month.year, month.month + 1, 1)

    end_date = datetime.combine(next_month, time.min)

    cost_trend = (
        db.query(
            DailyCost.date,
            func.sum(DailyCost.total_costs).label("total_cost")
        )
        .filter(
            DailyCost.date >= start_date,
            DailyCost.date < end_date
        )
        .group_by(DailyCost.date)
        .order_by(DailyCost.date)
        .all()
    )

    return cost_trend




def get_cost_by_service(db: Session, month):

    cost_by_service = (
        db.query(
            func.sum(MonthlyCost.dynamodb).label("dynamodb"),
            func.sum(MonthlyCost.sqs).label("sqs"),
            func.sum(MonthlyCost.glue).label("glue"),
            func.sum(MonthlyCost.ec2_instances).label("ec2_instances"),
            func.sum(MonthlyCost.elastic_container_service).label(
                "elastic_container_service"
            ),
            func.sum(MonthlyCost.iot).label("iot"),
            func.sum(MonthlyCost.ec2_other).label("ec2_other"),
            func.sum(MonthlyCost.s3).label("s3"),
            func.sum(MonthlyCost.cloudwatch).label("cloudwatch"),
            func.sum(MonthlyCost.vpc).label("vpc"),
            func.sum(MonthlyCost.lambda_cost).label("lambda_cost"),
            func.sum(
                MonthlyCost.documentdb_with_mongodb_compatibility
            ).label("documentdb"),
            func.sum(MonthlyCost.elastic_load_balancing).label(
                "elastic_load_balancing"
            ),
            func.sum(MonthlyCost.ec2_container_registry_ecr).label(
                "ec2_container_registry_ecr"
            ),
            func.sum(MonthlyCost.waf).label("waf"),
            func.sum(MonthlyCost.relational_database_service).label(
                "relational_database_service"
            ),
            func.sum(MonthlyCost.cost_explorer).label("cost_explorer"),
            func.sum(MonthlyCost.secrets_manager).label("secrets_manager"),
            func.sum(MonthlyCost.key_management_service).label(
                "key_management_service"
            ),
            func.sum(MonthlyCost.greengrass).label("greengrass"),
            func.sum(MonthlyCost.api_gateway).label("api_gateway"),
            func.sum(MonthlyCost.sns).label("sns"),
            func.sum(MonthlyCost.athena).label("athena"),
            func.sum(MonthlyCost.ses).label("ses"),
            func.sum(MonthlyCost.iot_device_management).label(
                "iot_device_management"
            ),
            func.sum(MonthlyCost.cloudshell).label("cloudshell"),
            func.sum(MonthlyCost.cloudformation).label("cloudformation"),
            func.sum(MonthlyCost.cloudwatch_events).label(
                "cloudwatch_events"
            ),
            func.sum(MonthlyCost.devopsagent).label("devopsagent"),
        )
        .filter(MonthlyCost.month_start == month)
        .first()
    )

    return cost_by_service






def get_cost_by_environment(db: Session, month):

    cost_by_environment = (
        db.query(
            AccountEnvironment.environment,
            func.sum(MonthlyCost.total_costs).label("total_cost")
        )
        .join(
            MonthlyCost,
            AccountEnvironment.account_id == MonthlyCost.account_id
        )
        .filter(
            MonthlyCost.month_start == month
        )
        .group_by(
            AccountEnvironment.environment
        )
        .all()
    )

    return cost_by_environment


def get_cost_forecast(db: Session, month: date):

    selected_month = datetime.combine(
        month,
        time.min
    )

    historical_data = (
        db.query(
            MonthlyCost.month_start,
            func.sum(MonthlyCost.total_costs).label("total_cost")
        )
        .filter(
            MonthlyCost.month_start <= selected_month
        )
        .group_by(
            MonthlyCost.month_start
        )
        .order_by(
            MonthlyCost.month_start
        )
        .all()
    )

    return historical_data