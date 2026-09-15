# from collections.abc import Sequence

# from sklearn.linear_model import LinearRegression


# MINIMUM_HISTORY_MONTHS = 6


# def forecast_next_month(historical_costs: Sequence[float]) -> float:
#     if len(historical_costs) < MINIMUM_HISTORY_MONTHS:
#         raise ValueError(
#             "At least 6 months of historical data are required "
#             "for forecasting."
#         )

#     costs = [float(cost) for cost in historical_costs]

#     # Month numbers: 1, 2, 3, ..., number of historical months
#     X = [[i] for i in range(1, len(costs) + 1)]

#     model = LinearRegression()
#     model.fit(X, costs)

#     # Predict the month immediately after the last historical month
#     next_month_number = len(costs) + 1
#     prediction = model.predict([[next_month_number]])

#     return round(max(0.0, float(prediction[0])), 2)


from collections.abc import Sequence
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
MODEL_VERSION = 3


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


def _train_and_save_model(cleaned_costs: list[float]) -> dict:
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

    next_month_number = len(cleaned_costs) + 1
    forecast_cost = model.predict([[next_month_number]])[0]

    artifact = {
        "version": MODEL_VERSION,
        "model": model,
        "historical_predictions": historical_predictions,
        "forecast_cost": round(max(0.0, float(forecast_cost)), 2),
    }
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, MODEL_PATH)
    return artifact


def forecast_next_month(
    historical_costs: Sequence[float],
) -> float:
    """
    Load the saved model, training it only when no model has been saved yet.
    """

    cleaned_costs = _clean_costs(historical_costs)

    if len(cleaned_costs) < 6:
        raise ValueError(
            "At least 6 months of historical data are required "
            "for forecasting."
        )

    if MODEL_PATH.exists():
        artifact = joblib.load(MODEL_PATH)
    else:
        artifact = None

    if (
        not artifact
        or artifact.get("version") != MODEL_VERSION
        or "forecast_cost" not in artifact
    ):
        artifact = _train_and_save_model(cleaned_costs)

    return artifact["forecast_cost"]