from sqlalchemy.orm import Session
from datetime import date

from app.dal.overview_dal import get_total_cost
from app.dal.overview_dal import get_total_accounts,get_average_daily_cost,get_cost_by_account
from app.dal.overview_dal import get_cost_trend,get_cost_by_environment
from app.dal.overview_dal import get_cost_by_service

from app.ml.cost_forecast.linear_regression import (
    forecast_next_month,
)


def calculate_overview(db: Session, month: date):

    total_cost = get_total_cost(db, month)

    total_accounts = get_total_accounts(db, month)

    average_daily_cost = get_average_daily_cost(db, month)

    return {
        "month": month,
        "total_cost": total_cost,
        "total_accounts": total_accounts,
        "average_daily_cost": round(average_daily_cost,2)
    }



def calculate_cost_by_account(db: Session, month: date):

    cost_by_account = get_cost_by_account(db, month)

    return [
        {
            "account_id": row.account_id,
            "account_name": row.account_name,
            "total_cost": round(row.total_costs or 0, 2)
        }
        for row in cost_by_account
    ]


def calculate_cost_trend(db:Session, month:date):

    cost_trend = get_cost_trend(db, month)

    return [
        {
            "date": row.date,
            "total_cost": round(row.total_cost or 0, 2)
        }
        for row in cost_trend
    ]


def calculate_cost_by_service(db: Session, month):

    result = get_cost_by_service(db, month)

    if not result:
        return []

    services = {
        "DynamoDB": result.dynamodb,
        "SQS": result.sqs,
        "Glue": result.glue,
        "EC2 Instances": result.ec2_instances,
        "Elastic Container Service": result.elastic_container_service,
        "IoT": result.iot,
        "EC2 Other": result.ec2_other,
        "S3": result.s3,
        "CloudWatch": result.cloudwatch,
        "VPC": result.vpc,
        "Lambda": result.lambda_cost,
        "DocumentDB": result.documentdb,
        "Elastic Load Balancing": result.elastic_load_balancing,
        "ECR": result.ec2_container_registry_ecr,
        "WAF": result.waf,
        "RDS": result.relational_database_service,
        "Cost Explorer": result.cost_explorer,
        "Secrets Manager": result.secrets_manager,
        "KMS": result.key_management_service,
        "Greengrass": result.greengrass,
        "API Gateway": result.api_gateway,
        "SNS": result.sns,
        "Athena": result.athena,
        "SES": result.ses,
        "IoT Device Management": result.iot_device_management,
        "CloudShell": result.cloudshell,
        "CloudFormation": result.cloudformation,
        "CloudWatch Events": result.cloudwatch_events,
        "DevOpsAgent": result.devopsagent,
    }

    
    services = {
        service: cost or 0
        for service, cost in services.items()
    }

    sorted_services = sorted(
        services.items(),
        key=lambda item: item[1],
        reverse=True
    )

    
    top_5 = sorted_services[:5]

    others = sum(
        cost
        for service, cost in sorted_services[5:]
    )

    response = [
        {
            "service": service,
            "total_cost": round(cost, 2)
        }
        for service, cost in top_5
    ]

    if others > 0:
        response.append(
            {
                "service": "Others",
                "total_cost": round(others, 2)
            }
        )

    return response



def calculate_cost_by_environment(db: Session, month):

    cost_by_environment = get_cost_by_environment(db, month)

    return [
        {
            "environment": row.environment,
            "total_cost": round(row.total_cost or 0, 2)
        }
        for row in cost_by_environment
    ]




def calculate_cost_forecast(
    db: Session,
    month: date,
):
    """
    Get historical costs and return the predicted
    cost for the next month.
    """

    if month.month == 12:
        next_month = date(
            month.year + 1,
            1,
            1,
        )
    else:
        next_month = date(
            month.year,
            month.month + 1,
            1,
        )

    forecast_cost = forecast_next_month(next_month)

    return {
        "month": next_month,
        "forecast_cost": forecast_cost,
    }
