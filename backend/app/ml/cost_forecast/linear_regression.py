from collections.abc import Sequence
from datetime import date
from math import isfinite
from pathlib import Path

import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

MODEL_PATH = Path(__file__).with_name("linear_regression_model.joblib")
MODEL_VERSION = 5


def _clean_costs(historical_costs: Sequence[float]) -> list[float]:
    cleaned_costs = []

    for cost in historical_costs:
        try:
            numeric_cost = float(cost)
        except (TypeError, ValueError):
            continue

        if isfinite(numeric_cost):
            cleaned_costs.append(numeric_cost)

    return cleaned_costs


def train_and_save_model(
    historical_costs: Sequence[float],
    first_month: date,
) -> dict:
    cleaned_costs = _clean_costs(historical_costs)

    if len(cleaned_costs) < 6:
        raise ValueError(
            "At least 6 months of historical data are required "
            "for forecasting."
        )

    actual_values = []
    predicted_values = []
    historical_predictions = {}

    for test_index in range(6, len(cleaned_costs)):
        train_costs = cleaned_costs[:test_index]
        actual_cost = cleaned_costs[test_index]
        X_train = [
            [month_number]
            for month_number in range(1, len(train_costs) + 1)
        ]

        validation_model = LinearRegression()
        validation_model.fit(X_train, train_costs)
        predicted_cost = validation_model.predict(
            [[len(train_costs) + 1]]
        )[0]

        actual_values.append(actual_cost)
        predicted_values.append(float(predicted_cost))
        historical_predictions[str(test_index + 1)] = round(
            max(0.0, float(predicted_cost)),
            2,
        )

    if actual_values:
        mae = mean_absolute_error(actual_values, predicted_values)
        mse = mean_squared_error(actual_values, predicted_values)
        r2_value = (
            r2_score(actual_values, predicted_values)
            if len(actual_values) >= 2
            else None
        )

        print("Model validation result:")
        print(f"MAE: {mae:.2f}")
        print(f"RMSE: {mse ** 0.5:.2f}")
        print(
            f"R2 Score: {r2_value:.4f}"
            if r2_value is not None
            else "R2 Score: Not enough validation data"
        )
    else:
        print(
            "Model validation skipped because there is "
            "not enough validation data."
        )

    X_final = [
        [month_number]
        for month_number in range(1, len(cleaned_costs) + 1)
    ]
    model = LinearRegression()
    model.fit(X_final, cleaned_costs)

    artifact = {
        "version": MODEL_VERSION,
        "model": model,
        "historical_costs": cleaned_costs,
        "first_month": first_month.isoformat(),
    }
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, MODEL_PATH)
    return artifact


def ensure_model(
    historical_costs: Sequence[float],
    first_month: date,
) -> None:
    cleaned_costs = _clean_costs(historical_costs)

    if len(cleaned_costs) < 6:
        return

    artifact = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None

    if (
        not artifact
        or artifact.get("version") != MODEL_VERSION
        or artifact.get("historical_costs") != cleaned_costs
        or artifact.get("first_month") != first_month.isoformat()
    ):
        train_and_save_model(cleaned_costs, first_month)


def forecast_next_month(month: date) -> float:
    """
    Load the model trained during application startup.
    """
    artifact = joblib.load(MODEL_PATH)
    first_month = date.fromisoformat(artifact["first_month"])
    month_number = (
        (month.year - first_month.year) * 12
        + month.month - first_month.month
        + 1
    )
    forecast_cost = artifact["model"].predict([[month_number]])[0]
    return round(max(0.0, float(forecast_cost)), 2)