from fastapi import FastAPI

from app.api.overview import router as overview_router
from app.api.accounts import router as accounts_router
from app.database.database import SessionLocal
from app.dal.overview_dal import get_all_cost_forecast
from app.ml.cost_forecast.linear_regression import ensure_model

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AWS Dashboard Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
    "http://localhost",
    "https://aws-dashboard-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def initialize_forecast_model():
    db = SessionLocal()
    try:
        rows = get_all_cost_forecast(db)
        if rows:
            historical_costs = [
                float(row.total_cost)
                for row in rows
                if row.total_cost is not None
            ]
            ensure_model(historical_costs, rows[0].month_start.date())
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "HELLO OBITO"}


app.include_router(overview_router)
app.include_router(accounts_router)