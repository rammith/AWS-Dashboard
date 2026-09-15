from sqlalchemy import Column, String
from app.database.database import Base


class AccountEnvironment(Base):
    __tablename__ = "account_environment"

    account_id = Column(String, primary_key=True)
    account_name = Column(String)
    environment = Column(String)