import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from fastapi.testclient import TestClient

from app.database.database import get_db
from app.main import app
import app.api.overview as overview_api
import app.api.accounts as accounts_api

client = TestClient(app)


def override_get_db():
    yield None


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "HELLO OBITO"}


def test_overview_total_endpoint(monkeypatch):
    original = overview_api.get_overview_controller

    def fake_controller(db, month):
        assert db is None
        assert str(month) == "2025-08-01"
        return {
            "month": "2025-08-01",
            "total_cost": 1200,
            "total_accounts": 5,
            "average_daily_cost": 40.0,
        }

    monkeypatch.setattr(overview_api, "get_overview_controller", fake_controller)
    app.dependency_overrides[get_db] = override_get_db

    try:
        response = client.get("/api/overview/total?month=2025-08-01")
        assert response.status_code == 200
        assert response.json()["total_cost"] == 1200
        assert response.json()["total_accounts"] == 5
    finally:
        app.dependency_overrides.clear()
        monkeypatch.setattr(overview_api, "get_overview_controller", original)


def test_accounts_summary_endpoint(monkeypatch):
    original = accounts_api.get_account_summary_controller

    def fake_controller(db, month):
        assert db is None
        assert str(month) == "2025-08-01"
        return {
            "month": "2025-08-01",
            "total_accounts": 3,
            "total_monthly_cost": 800.0,
            "average_monthly_cost_per_account": 266.67,
        }

    monkeypatch.setattr(accounts_api, "get_account_summary_controller", fake_controller)
    app.dependency_overrides[get_db] = override_get_db

    try:
        response = client.get("/api/accounts/summary?month=2025-08-01")
        assert response.status_code == 200
        assert response.json()["total_accounts"] == 3
        assert response.json()["average_monthly_cost_per_account"] == 266.67
    finally:
        app.dependency_overrides.clear()
        monkeypatch.setattr(accounts_api, "get_account_summary_controller", original)
