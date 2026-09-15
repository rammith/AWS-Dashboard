from datetime import date

from app.services.account_service import calculate_account_summary, calculate_accounts


class FakeRow:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class FakeDB:
    pass


def test_calculate_account_summary_returns_expected_values():
    db = FakeDB()
    month = date(2025, 8, 1)

    def fake_get_total_accounts(_, __):
        return 3

    def fake_get_total_monthly_cost(_, __):
        return 1500.0

    import app.services.account_service as account_service

    original_total_accounts = account_service.get_total_accounts
    original_total_monthly_cost = account_service.get_total_monthly_cost

    account_service.get_total_accounts = fake_get_total_accounts
    account_service.get_total_monthly_cost = fake_get_total_monthly_cost

    try:
        result = calculate_account_summary(db, month)
    finally:
        account_service.get_total_accounts = original_total_accounts
        account_service.get_total_monthly_cost = original_total_monthly_cost

    assert result == {
        "month": month,
        "total_accounts": 3,
        "total_monthly_cost": 1500.0,
        "average_monthly_cost_per_account": 500.0,
    }


def test_calculate_accounts_handles_no_previous_data_and_increase():
    db = FakeDB()
    month = date(2025, 8, 1)

    account_rows = [
        {
            "account_id": "a-001",
            "account_name": "Production",
            "environment": "Production",
            "monthly_cost": 500.0,
            "previous_cost": 0,
        },
        {
            "account_id": "a-002",
            "account_name": "Dev",
            "environment": "Development",
            "monthly_cost": 400.0,
            "previous_cost": 200.0,
        },
    ]

    import app.services.account_service as account_service

    original = account_service.get_accounts_with_cost_and_trend
    account_service.get_accounts_with_cost_and_trend = lambda _, __: account_rows

    try:
        result = calculate_accounts(db, month)
    finally:
        account_service.get_accounts_with_cost_and_trend = original

    assert result[0]["trend_direction"] == "no_previous_data"
    assert result[0]["trend_percentage"] is None
    assert result[1]["trend_direction"] == "increase"
    assert result[1]["trend_percentage"] == 100.0
