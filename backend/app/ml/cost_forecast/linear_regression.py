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

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


def forecast_next_month(
    historical_costs: Sequence[float],
) -> float:
    """
    Train Linear Regression, validate the model internally,
    and return only the predicted next-month cost.
    """

    # --------------------------------------------------
    # 1. Clean historical cost values
    # --------------------------------------------------

    cleaned_costs = []

    for cost in historical_costs:
        try:
            numeric_cost = float(cost)
        except (TypeError, ValueError):
            continue

        if not isfinite(numeric_cost):
            continue

        cleaned_costs.append(numeric_cost)

    # --------------------------------------------------
    # 2. Check minimum six months
    # --------------------------------------------------

    if len(cleaned_costs) < 6:
        raise ValueError(
            "At least 6 months of historical data are required "
            "for forecasting."
        )

    # --------------------------------------------------
    # 3. Validate the model using walk-forward validation
    # --------------------------------------------------

    actual_values = []
    predicted_values = []

    for test_index in range(6, len(cleaned_costs)):
        train_costs = cleaned_costs[:test_index]
        actual_cost = cleaned_costs[test_index]

        # Month numbers for training data.
        X_train = [
            [month_number]
            for month_number in range(1, len(train_costs) + 1)
        ]

        model = LinearRegression()
        model.fit(X_train, train_costs)

        # Predict the next month after the training data.
        next_month_number = len(train_costs) + 1

        predicted_cost = model.predict(
            [[next_month_number]]
        )[0]

        actual_values.append(actual_cost)
        predicted_values.append(float(predicted_cost))

    # --------------------------------------------------
    # 4. Calculate validation metrics internally
    # --------------------------------------------------

    if actual_values:
        mae = mean_absolute_error(
            actual_values,
            predicted_values,
        )

        mse = mean_squared_error(
            actual_values,
            predicted_values,
        )

        rmse = mse ** 0.5

        if len(actual_values) >= 2:
            r2_value = r2_score(
                actual_values,
                predicted_values,
            )
        else:
            r2_value = None

        print("Model validation result:")
        print(f"MAE: {mae:.2f}")
        print(f"RMSE: {rmse:.2f}")

        if r2_value is not None:
            print(f"R2 Score: {r2_value:.4f}")
        else:
            print("R2 Score: Not enough validation data")

    else:
        print(
            "Model validation skipped because there is "
            "not enough validation data."
        )

    # --------------------------------------------------
    # 5. Train the final model using all historical data
    # --------------------------------------------------

    X_final = [
        [month_number]
        for month_number in range(1, len(cleaned_costs) + 1)
    ]

    final_model = LinearRegression()
    final_model.fit(
        X_final,
        cleaned_costs,
    )

    # --------------------------------------------------
    # 6. Predict the next month
    # --------------------------------------------------

    next_month_number = len(cleaned_costs) + 1

    forecast_cost = final_model.predict(
        [[next_month_number]]
    )[0]

    # Avoid returning a negative forecast.
    forecast_cost = max(0.0, float(forecast_cost))

    return round(forecast_cost, 2)