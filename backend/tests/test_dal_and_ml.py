from datetime import date

import pytest

from app.dal.account_dal import (
    get_total_accounts,
    get_total_monthly_cost,
    get_accounts_with_cost_and_trend,
)
from app.dal.overview_dal import (
    get_total_cost,
    get_total_accounts as overview_total_accounts,
    get_average_daily_cost,
    get_cost_by_account,
    get_cost_trend,
    get_cost_by_service,
    get_cost_by_environment,
    get_cost_forecast,
)
from app.ml.cost_forecast.linear_regression import forecast_next_month


class FakeRow:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getitem__(self, key):
        return self.__dict__[key]


class FakeQuery:
    def __init__(self, result=None, value=None, subquery_result=None):
        self.result = result
        self.value = value
        self.subquery_result = subquery_result

    def join(self, *args, **kwargs):
        return self

    def filter(self, *args, **kwargs):
        return self

    def group_by(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def subquery(self):
        return self.subquery_result if self.subquery_result is not None else self

    def all(self):
        return self.result or []

    def first(self):
        return self.result

    def scalar(self):
        return self.value


class FakeAccountDB:
    def __init__(self, scalar_value=None, current_rows=None, previous_rows=None):
        self.scalar_value = scalar_value
        self.current_rows = current_rows or []
        self.previous_rows = previous_rows or []
        self._step = 0

    def query(self, *args, **kwargs):
        self._step += 1
        if self._step == 1:
            return FakeQuery(value=self.scalar_value, result=self.current_rows)
        return FakeQuery(result=self.previous_rows)


class FakeOverviewDB:
    def __init__(self, scalar_value=None, rows=None, trend_rows=None, env_rows=None, forecast_rows=None):
        self.scalar_value = scalar_value
        self.rows = rows or []
        self.trend_rows = trend_rows or []
        self.env_rows = env_rows or []
        self.forecast_rows = forecast_rows or []
        self._step = 0

    def query(self, *args, **kwargs):
        self._step += 1
        if self._step == 1:
            return FakeQuery(value=self.scalar_value, subquery_result=FakeSubquery())
        if self._step == 2:
            return FakeQuery(value=self.scalar_value)
        if self._step == 3:
            return FakeQuery(result=self.rows)
        if self._step == 4:
            return FakeQuery(result=self.trend_rows)
        if self._step == 5:
            return FakeQuery(result=FakeRow(
                dynamodb=500,
                sqs=200,
                glue=100,
                ec2_instances=80,
                elastic_container_service=60,
                iot=40,
                ec2_other=30,
                s3=20,
                cloudwatch=15,
                vpc=10,
                lambda_cost=5,
                documentdb=4,
                elastic_load_balancing=3,
                ec2_container_registry_ecr=2,
                waf=1,
                relational_database_service=1,
                cost_explorer=1,
                secrets_manager=1,
                key_management_service=1,
                greengrass=1,
                api_gateway=1,
                sns=1,
                athena=1,
                ses=1,
                iot_device_management=1,
                cloudshell=1,
                cloudformation=1,
                cloudwatch_events=1,
                devopsagent=1,
            ))
        if self._step == 6:
            return FakeQuery(result=self.env_rows)
        return FakeQuery(result=self.forecast_rows)


class FakeSubquery:
    class _DailyTotal:
        daily_total = 2500

    c = _DailyTotal()


def test_account_dal_total_queries_and_previous_month_mapping():
    current_rows = [
        FakeRow(account_id='acc-1', account_name='Prod', environment='Production', monthly_cost=500, previous_cost=300),
        FakeRow(account_id='acc-2', account_name='Dev', environment='Development', monthly_cost=200, previous_cost=250),
    ]
    previous_rows = [
        FakeRow(account_id='acc-1', previous_cost=300),
        FakeRow(account_id='acc-2', previous_cost=250),
    ]

    total_db = FakeAccountDB(scalar_value=5)
    assert get_total_accounts(total_db, date(2025, 2, 1)) == 5

    total_cost_db = FakeAccountDB(scalar_value=2300)
    assert get_total_monthly_cost(total_cost_db, date(2025, 2, 1)) == 2300

    account_db = FakeAccountDB(current_rows=current_rows, previous_rows=previous_rows)
    result = get_accounts_with_cost_and_trend(account_db, date(2025, 2, 1))
    assert result[0]['account_id'] == 'acc-1'
    assert result[0]['previous_cost'] == 300
    assert result[0]['monthly_cost'] == 500
    assert result[1]['previous_cost'] == 250


def test_overview_dal_queries_and_cost_breakdowns():
    db = FakeOverviewDB(
        scalar_value=1500,
        rows=[
            FakeRow(account_id='acc-1', account_name='Prod', total_costs=1200),
            FakeRow(account_id='acc-2', account_name='Dev', total_costs=300),
        ],
        trend_rows=[
            FakeRow(date='2025-08-01', total_cost=1200),
            FakeRow(date='2025-08-02', total_cost=1300),
        ],
        env_rows=[
            FakeRow(environment='Production', total_cost=1000),
            FakeRow(environment='Development', total_cost=300),
        ],
        forecast_rows=[
            FakeRow(month_start=date(2025, 1, 1), total_cost=1000),
            FakeRow(month_start=date(2025, 2, 1), total_cost=1200),
            FakeRow(month_start=date(2025, 3, 1), total_cost=1300),
            FakeRow(month_start=date(2025, 4, 1), total_cost=1400),
            FakeRow(month_start=date(2025, 5, 1), total_cost=1500),
            FakeRow(month_start=date(2025, 6, 1), total_cost=1600),
        ],
    )

    assert get_total_cost(db, date(2025, 8, 1)) == 1500
    assert overview_total_accounts(db, date(2025, 8, 1)) == 1500

    zero_db = FakeOverviewDB(scalar_value=None)
    assert overview_total_accounts(zero_db, date(2025, 8, 1)) == 0

    avg_db = FakeOverviewDB(scalar_value=2500)
    assert get_average_daily_cost(avg_db, date(2025, 8, 1)) == 2500

    accounts = get_cost_by_account(db, date(2025, 8, 1))
    assert accounts[0].account_id == 'acc-1'
    assert accounts[1].account_name == 'Dev'

    trend = get_cost_trend(db, date(2025, 8, 1))
    assert len(trend) == 2
    assert trend[0].date == '2025-08-01'

    service_data = get_cost_by_service(db, date(2025, 8, 1))
    assert service_data.dynamodb == 500
    assert service_data.sqs == 200

    env_data = get_cost_by_environment(db, date(2025, 8, 1))
    assert env_data[0].environment == 'Production'
    assert env_data[1].total_cost == 300

    forecast_data = get_cost_forecast(db, date(2025, 6, 1))
    assert len(forecast_data) == 6
    assert forecast_data[0].total_cost == 1000


def test_ml_forecast_next_month_handles_valid_history_and_short_history():
    valid_history = [1000, 1100, 1250, 1300, 1450, 1500, 1600, 1750]
    result = forecast_next_month(valid_history)
    assert result > 0

    with pytest.raises(ValueError):
        forecast_next_month([100, 200, 300, 400, 500])
