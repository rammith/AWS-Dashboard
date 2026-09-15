from datetime import date

from app.services.overview_service import (
    calculate_total_cost,
    calculate_total_accounts,
    calculate_average_daily_cost,
    calculate_overview,
    calculate_cost_by_account,
    calculate_cost_trend,
    calculate_cost_by_service,
    calculate_cost_by_environment,
)


class FakeRow:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class FakeDB:
    pass


def test_calculate_total_cost_rounds_value():
    db = FakeDB()
    month = date(2025, 8, 1)

    import app.services.overview_service as overview_service

    original = overview_service.get_total_cost
    overview_service.get_total_cost = lambda _, __: 1234.567

    try:
        assert calculate_total_cost(db, month) == 1234.57
    finally:
        overview_service.get_total_cost = original


def test_calculate_overview_returns_summary():
    db = FakeDB()
    month = date(2025, 8, 1)

    import app.services.overview_service as overview_service

    original_total_cost = overview_service.get_total_cost
    original_total_accounts = overview_service.get_total_accounts
    original_average_daily_cost = overview_service.get_average_daily_cost

    overview_service.get_total_cost = lambda _, __: 2400.0
    overview_service.get_total_accounts = lambda _, __: 12
    overview_service.get_average_daily_cost = lambda _, __: 80.0

    try:
        result = calculate_overview(db, month)
    finally:
        overview_service.get_total_cost = original_total_cost
        overview_service.get_total_accounts = original_total_accounts
        overview_service.get_average_daily_cost = original_average_daily_cost

    assert result == {
        "month": month,
        "total_cost": 2400.0,
        "total_accounts": 12,
        "average_daily_cost": 80.0,
    }


def test_calculate_cost_by_account_maps_rows():
    db = FakeDB()
    month = date(2025, 8, 1)

    import app.services.overview_service as overview_service

    original = overview_service.get_cost_by_account
    overview_service.get_cost_by_account = lambda _, __: [
        FakeRow(account_id="A-1", account_name="Main", total_costs=123.456),
        FakeRow(account_id="A-2", account_name="Backup", total_costs=None),
    ]

    try:
        result = calculate_cost_by_account(db, month)
    finally:
        overview_service.get_cost_by_account = original

    assert result == [
        {"account_id": "A-1", "account_name": "Main", "total_cost": 123.46},
        {"account_id": "A-2", "account_name": "Backup", "total_cost": 0},
    ]


def test_calculate_cost_trend_maps_rows():
    db = FakeDB()
    month = date(2025, 8, 1)

    import app.services.overview_service as overview_service

    original = overview_service.get_cost_trend
    overview_service.get_cost_trend = lambda _, __: [
        FakeRow(date="2025-08-01", total_cost=100.0),
        FakeRow(date="2025-08-02", total_cost=150.5),
    ]

    try:
        result = calculate_cost_trend(db, month)
    finally:
        overview_service.get_cost_trend = original

    assert result == [
        {"date": "2025-08-01", "total_cost": 100.0},
        {"date": "2025-08-02", "total_cost": 150.5},
    ]


def test_calculate_cost_by_service_returns_top_services_and_others():
    db = FakeDB()
    month = date(2025, 8, 1)

    import app.services.overview_service as overview_service

    original = overview_service.get_cost_by_service
    overview_service.get_cost_by_service = lambda _, __: FakeRow(
        dynamodb=50,
        sqs=40,
        glue=30,
        ec2_instances=20,
        elastic_container_service=10,
        iot=8,
        ec2_other=7,
        s3=6,
        cloudwatch=5,
        vpc=4,
        lambda_cost=3,
        documentdb=2,
        elastic_load_balancing=1,
        ec2_container_registry_ecr=0,
        waf=0,
        relational_database_service=0,
        cost_explorer=0,
        secrets_manager=0,
        key_management_service=0,
        greengrass=0,
        api_gateway=0,
        sns=0,
        athena=0,
        ses=0,
        iot_device_management=0,
        cloudshell=0,
        cloudformation=0,
        cloudwatch_events=0,
        devopsagent=0,
    )

    try:
        result = calculate_cost_by_service(db, month)
    finally:
        overview_service.get_cost_by_service = original

    assert result[0]["service"] == "DynamoDB"
    assert result[0]["total_cost"] == 50
    assert result[-1]["service"] == "Others"


def test_calculate_cost_by_environment_maps_rows():
    db = FakeDB()
    month = date(2025, 8, 1)

    import app.services.overview_service as overview_service

    original = overview_service.get_cost_by_environment
    overview_service.get_cost_by_environment = lambda _, __: [
        FakeRow(environment="Production", total_cost=1000),
        FakeRow(environment="Development", total_cost=300),
    ]

    try:
        result = calculate_cost_by_environment(db, month)
    finally:
        overview_service.get_cost_by_environment = original

    assert result == [
        {"environment": "Production", "total_cost": 1000.0},
        {"environment": "Development", "total_cost": 300.0},
    ]


def test_calculate_total_accounts_and_average_daily_cost():
    db = FakeDB()
    month = date(2025, 8, 1)

    import app.services.overview_service as overview_service

    original_total_accounts = overview_service.get_total_accounts
    original_average_daily_cost = overview_service.get_average_daily_cost

    overview_service.get_total_accounts = lambda _, __: 9
    overview_service.get_average_daily_cost = lambda _, __: 75.25

    try:
        assert calculate_total_accounts(db, month) == 9
        assert calculate_average_daily_cost(db, month) == 75.25
    finally:
        overview_service.get_total_accounts = original_total_accounts
        overview_service.get_average_daily_cost = original_average_daily_cost
