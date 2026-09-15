from fastapi import FastAPI

from app.api.overview import router as overview_router
from app.api.accounts import router as accounts_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
    "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "HELLO OBITO"}


app.include_router(overview_router)
app.include_router(accounts_router)