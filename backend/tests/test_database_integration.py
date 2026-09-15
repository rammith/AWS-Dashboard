from datetime import date

from app.services.account_service import calculate_account_summary, calculate_accounts
from app.services.overview_service import calculate_overview, calculate_cost_by_account


class FakeAccountQueryResult:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getitem__(self, key):
        return self.__dict__[key]


class FakeDB:
    def __init__(self):
        self.account_rows = [
            FakeAccountQueryResult(
                account_id="A-001",
                account_name="Production",
                environment="Production",
                monthly_cost=1100.0,
                previous_cost=900.0,
            ),
            FakeAccountQueryResult(
                account_id="A-002",
                account_name="Dev",
                environment="Development",
                monthly_cost=250.0,
                previous_cost=200.0,
            ),
        ]
        self.overview_rows = [
            FakeAccountQueryResult(total_cost=1350.0),
        ]


def test_calculate_account_summary_with_mocked_db():
    db = FakeDB()
    month = date(2025, 8, 1)

    import app.services.account_service as account_service

    original_total_accounts = account_service.get_total_accounts
    original_total_monthly_cost = account_service.get_total_monthly_cost
    original_accounts = account_service.get_accounts_with_cost_and_trend

    account_service.get_total_accounts = lambda _, __: 2
    account_service.get_total_monthly_cost = lambda _, __: 1350.0
    account_service.get_accounts_with_cost_and_trend = lambda _, __: db.account_rows

    try:
        summary = calculate_account_summary(db, month)
        accounts = calculate_accounts(db, month)
    finally:
        account_service.get_total_accounts = original_total_accounts
        account_service.get_total_monthly_cost = original_total_monthly_cost
        account_service.get_accounts_with_cost_and_trend = original_accounts

    assert summary["total_accounts"] == 2
    assert summary["total_monthly_cost"] == 1350.0
    assert summary["average_monthly_cost_per_account"] == 675.0
    assert accounts[0]["trend_direction"] == "increase"
    assert accounts[0]["trend_percentage"] == 22.22


def test_calculate_overview_with_mocked_db():
    db = FakeDB()
    month = date(2025, 8, 1)

    import app.services.overview_service as overview_service

    original_total_cost = overview_service.get_total_cost
    original_total_accounts = overview_service.get_total_accounts
    original_average_daily_cost = overview_service.get_average_daily_cost
    original_cost_by_account = overview_service.get_cost_by_account

    overview_service.get_total_cost = lambda _, __: 1350.0
    overview_service.get_total_accounts = lambda _, __: 2
    overview_service.get_average_daily_cost = lambda _, __: 43.55
    overview_service.get_cost_by_account = lambda _, __: [
        FakeAccountQueryResult(account_id="A-001", account_name="Production", total_costs=1100.0),
        FakeAccountQueryResult(account_id="A-002", account_name="Dev", total_costs=250.0),
    ]

    try:
        overview = calculate_overview(db, month)
        account_costs = calculate_cost_by_account(db, month)
    finally:
        overview_service.get_total_cost = original_total_cost
        overview_service.get_total_accounts = original_total_accounts
        overview_service.get_average_daily_cost = original_average_daily_cost
        overview_service.get_cost_by_account = original_cost_by_account

    assert overview["total_cost"] == 1350.0
    assert overview["total_accounts"] == 2
    assert overview["average_daily_cost"] == 43.55
    assert account_costs[0]["account_name"] == "Production"
    assert account_costs[1]["total_cost"] == 250.0
