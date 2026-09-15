from sqlalchemy import Column, String, DateTime, Float
from app.database.database import Base


class WeeklyCost(Base):
    __tablename__ = "weekly_costs"

    account_id = Column(String, primary_key=True)
    account_name = Column(String)
    week_start = Column(DateTime, primary_key=True)

    dynamodb = Column(Float)
    tax = Column(Float)
    sqs = Column(Float)
    glue = Column(Float)
    ec2_instances = Column(Float)
    elastic_container_service = Column(Float)
    iot = Column(Float)
    ec2_other = Column(Float)
    s3 = Column(Float)
    cloudwatch = Column(Float)
    vpc = Column(Float)
    lambda_cost = Column("lambda", Float)
    documentdb_with_mongodb_compatibility = Column(
        "documentdb_(with_mongodb_compatibility)", Float
    )
    elastic_load_balancing = Column(Float)
    ec2_container_registry_ecr = Column(
        "ec2_container_registry_(ecr)", Float
    )
    waf = Column(Float)
    relational_database_service = Column(Float)
    cost_explorer = Column(Float)
    secrets_manager = Column(Float)
    key_management_service = Column(Float)
    greengrass = Column(Float)
    api_gateway = Column(Float)
    sns = Column(Float)
    athena = Column(Float)
    ses = Column(Float)
    iot_device_management = Column(Float)
    cloudshell = Column(Float)
    cloudformation = Column(Float)
    cloudwatch_events = Column(Float)
    devopsagent = Column(Float)
    total_costs = Column(Float)